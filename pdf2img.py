import os, glob
from tqdm import tqdm
from pdf2image import convert_from_path, convert_from_bytes

# n = 0
for pdf_file in tqdm(glob.glob("ds_pdf/*.pdf")):
    file_name = os.path.splitext(os.path.basename(pdf_file))[0]
    pages = convert_from_path(pdf_file)

    for no, page in enumerate(pages):
        image_name =  file_name + "_" + str(no) + ".jpeg"
        page.save(os.path.join("ds_set_images", image_name), 'JPEG')