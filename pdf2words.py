import pdfplumber
import glob, pickle, os
from tqdm import tqdm
import numpy as np


def get_pages_and_words_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        extracted_pages = []
        for page in pdf.pages:
            words = page.extract_words(x_tolerance=2, y_tolerance=2, horizontal_ltr=True, vertical_ttb=True)

            img = page.to_image().original
            np_img = np.array(img)


            formatted_words_list = []
            for no, word in enumerate(words):
                x1 = int(word["x0"])
                y1 = int(word["top"])
                x2 = int(word["x1"])
                y2 = int(word["bottom"])
                text = word["text"]
                formatted_words_list.append([x1, y1, x2, y2, text])
            extracted_pages.append({
                "width": np_img.shape[1],
                "height": np_img.shape[0],
                "words": formatted_words_list
            })

    return extracted_pages

if __name__ == "__main__":
    for pdf_file in tqdm(glob.glob("ds_pdf/*.pdf")):
        val = get_pages_and_words_from_pdf(pdf_file)
        for idx, v in enumerate(val):
            file_name = os.path.splitext(os.path.basename(pdf_file))[0]
            with open(os.path.join('set_1_pickles', f'{file_name}_{idx}.pickle'), 'wb') as f:
                print(v)
                pickle.dump(v, f)
