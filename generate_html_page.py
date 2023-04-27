def generate_html_code(header_text, field_name, text_list, n_samples, target_texts, audio_files_list):
    html_code = f"""
    <div class="container pt-5 mt-5 shadow p-5 mb-5 bg-white rounded">
        <h2 id="my-id" style="text-align: center;">{header_text}</h2>
        <div class="table-responsive pt-3">
            <table class="table table-hover pt-2">
                <thead>
                    <tr>
                        <th style="text-align: center"></th>
                        <th style="text-align: center; width=200px">Prompt Text</th>
                        <th style="text-align: center">Prompt</th>"""
    for sample_id in range(1, n_samples + 1):
        html_code += f"""
                        <th style="text-align: center">Sample #{sample_id}</th>"""
    html_code += f"""
                    </tr>
                </thead>
                <tbody>"""
    n_columns = 3 + n_samples
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
                        <td style="text-align: center;vertical-align:middle">{field_name} #{i}</td>
                        <td style="text-align: center;vertical-align:middle;"><font size="1">{text_list[i-1]}</font></td>
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
    html_code += """
                </tbody>
            </table>
        </div>
    </div>
    """
    return html_code

def dump_html_dummy(main_dir, n_samples=3):

    html_code = ""
    for dur in [3, 6, 10]:
        header_text = f"Voice Prompting ({dur} sec)"
        field_name = "Speaker"
        target_texts = []
        audio_lists = []
        for target_id in range(3):
            aud_list = []
            text_list = []
            for dataset in ["dev_other", "dev_clean"]:
                for gender in ["m", "f"]:
                    fprefix = f"{dataset}/{gender}/{dur}/{target_id}"
                    with open(f"{main_dir}/{fprefix}/prompt.txt", "r") as fpr:
                        prompt = fpr.readlines()[0].strip()
                    with open(f"{main_dir}/{fprefix}/target.txt", "r") as ftr:
                        target = ftr.readlines()[0].strip()
                    aud_list.append(f"{main_dir}/{fprefix}")
                    text_list.append(prompt.capitalize())
            audio_lists.append(aud_list)
            target_texts.append(target)

        html_code += """

        """
        html_code += generate_html_code(header_text, field_name, text_list, n_samples, target_texts, audio_lists)
    return html_code

if __name__ == "__main__":

    main_dir = "audios/mono_style_transfer"
    with open("dummy.html", "w") as fd:
        print(dump_html_dummy(main_dir), file=fd)
