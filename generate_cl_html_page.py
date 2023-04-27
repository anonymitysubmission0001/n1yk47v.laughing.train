def generate_html_head(header_text, n_samples):
    html_code = f"""
    <div class="container pt-5 mt-5 shadow p-5 mb-5 bg-white rounded">
        <h2 id="my-id" style="text-align: center;">{header_text}</h2>
        <div class="table-responsive pt-3">
            <table class="table table-hover pt-2">
                <thead>
                    <tr>
                        <th style="text-align: center; width=200px">Prompt Gender</th>
                        <th style="text-align: center">Original Gender</th>
                        <th style="text-align: center"></th>
                        <th style="text-align: center; width=200px">Original
                        Voice</th>
                        <th style="text-align: center">Prompt Voice</th>"""
    for sample_id in range(1, n_samples + 1):
        html_code += f"""
                        <th style="text-align: center">Sample {sample_id}</th>"""
    html_code += f"""
                    </tr>
                </thead>
                <tbody>"""
    return html_code


def generate_html_tail():
    html_code = """
                </tbody>
            </table>
        </div>
    </div>
    """
    return html_code

def generate_html_body(src_language, target_language, src_gender,
                       target_gender, text_list, n_samples, target_texts,
                       audio_files_list, skip_language_head=False):
    n_columns = 5 + n_samples
    html_code = ""
    if not skip_language_head:
        html_code += f"""
                    <tr>
                        <td colspan="{n_columns}" style="text-align: center">
                            <font size="3"><strong>{src_language} to
                            {target_language}</strong></font>
                        </td>
                    </tr>"""
    for target_idx, target_text in enumerate(target_texts):
        audio_files = audio_files_list[target_idx]
        html_code += f"""
                    <tr>
                        <td colspan="{n_columns}" style="text-align: center">
                            <font size="2">Target Text: "{target_text}"</font>
                        </td>
                    </tr>"""

        for i, audio_file in enumerate(audio_files, 1):
            html_code += f"""
                    <tr>
                        <td style="text-align: center;vertical-align:middle;"><font size="1">{src_gender}</font></td>
                        <td style="text-align: center;vertical-align:middle;"><font size="1">{target_gender}</font></td>
                        <td style="text-align: center;vertical-align:middle;"><font size="1">{text_list[i-1]}</font></td>
                        <td style="text-align: center">
                            <audio controls="controls" style="width: 150px;">
                                <source src="{audio_file}/target.wav" autoplay/>Your browser does not support the audio element.
                            </audio>
                        </td>
                        <td style="text-align: center">
                            <audio controls="controls" style="width: 150px;">
                                <source src="{audio_file}/prompt.wav" autoplay/>Your browser does not support the audio element.
                            </audio>
                        </td>"""
            for sample_id in range(n_samples):
                html_code += f"""
                        <td style="text-align: center">
                            <audio controls="controls" style="width: 150px;">
                                <source src="{audio_file}/{sample_id}.wav" autoplay/>Your browser does not support the audio element.
                            </audio>
                        </td>"""
            html_code += f"""
                    </tr>"""
    return html_code

def generate_test_cases(languages):
    from itertools import product as itpr
    all_languages = languages
    test_cases_languages = []
    test_cases_paths = []
    test_cases_genders = []
    genders = ["m", "f"]
    genders_map = {
        "m": "Male",
        "f": "Female",
    }
    for l1, l2 in itpr(all_languages, all_languages):
        if l1 != l2:
            for g1, g2 in itpr(genders, genders):
                test_cases_languages.append([l1, l2])
                test_cases_paths.append(f"{l1}/{l2}/{g1}2{g2}")
                test_cases_genders.append([
                    genders_map[g1], genders_map[g2]
                ])
    return test_cases_languages, test_cases_paths, test_cases_genders

def dump_html_dummy(main_dir, languages, n_samples=3):
    test_cases_languages, test_cases_paths, test_cases_genders = generate_test_cases(languages)
    html_code = ""
    html_code += generate_html_head(header_text="Cross-Lingual Style Transfer",
                                    n_samples=n_samples)

    language_heads = set()
    for (src_language, target_language), tc_path, (src_gender, target_gender) in zip(test_cases_languages, test_cases_paths, test_cases_genders):
        with open(f"{main_dir}/{tc_path}/prompt.txt", "r") as fpr:
            prompt = fpr.readlines()[0].strip()
        with open(f"{main_dir}/{tc_path}/target.txt", "r") as ftr:
            target = ftr.readlines()[0].strip()
        prompt = prompt.replace('[','').replace(']','').replace('\'','').replace('\"','').capitalize()
        target = target.replace('[','').replace(']','').replace('\'','').replace('\"','').capitalize()

        aud_list = [f"{main_dir}/{tc_path}"]
        skip_language_head = f"{src_language}_{target_language}" in language_heads
        # skip_language_head = False
        language_heads.add(f"{src_language}_{target_language}")
        html_code += generate_html_body(src_language.capitalize(),
                                        target_language.capitalize(),
                                        src_gender, target_gender,
                                        [prompt], n_samples, [target],
                                        [aud_list], skip_language_head)

    html_code += generate_html_tail()
    return html_code

if __name__ == "__main__":

    languages = ["french", "english", "german", "polish", "spanish", "portuguese"]
    main_dir = "audios/cross_lingual_style_transfer"
    with open("dummy.html", "w") as fd:
        print(dump_html_dummy(main_dir, languages, n_samples=2), file=fd)
