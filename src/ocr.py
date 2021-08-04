import cv2
import pytesseract
import os
  
# To use this script on Windows:
# 1. Download Tesseract for Windows from https://github.com/UB-Mannheim/tesseract/wiki
# Or use this latest one: https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20210506.exe
# 2. Add the default Tesseract installation path to System Environment variable
# c:\Program Files\Tesseract-OCR\ 
# 3. Profit!
  
# Mention the installed location of Tesseract-OCR in your system
pytesseract.pytesseract.tesseract_cmd = 'tesseract.exe'

INPUT_DIR='input'
OUTPUT_DIR='output'

SEP = "--------------------"

def main():
    if not os.path.exists(INPUT_DIR):
        os.mkdir(INPUT_DIR)
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
      
    files = list_files(INPUT_DIR)
    totalFiles = len(files)
    print("Found %d files!" % totalFiles)
    print(SEP)
    fileIdx = 1
    for file in files:
        print("[%d/%d] OCR-ing file=%s" % (fileIdx, totalFiles, file))
        # Read image from which text needs to be extracted
        img = cv2.imread(file)
        
        # run ocr routine example 1 (best result)
        # ref: https://medium.com/@marioruizgonzalez.mx/how-install-tesseract-orc-and-pytesseract-on-windows-68f011ad8b9b
        text = ocr_routine_example_1(img)    
        
        # run ocr routine example 2 (another method)
        # ref: https://www.geeksforgeeks.org/text-detection-and-extraction-using-opencv-and-ocr/
        # ocr_routine_example_2(img)  
        
        # one file per input
        outFileName = os.path.splitext(os.path.basename(file))[0] + "-ocr.txt"
        outFilePath = os.path.join(OUTPUT_DIR, outFileName)
        with open(outFilePath, 'w',5 ,'utf-8') as text_file:
            print("[%d/%d] Save to text file=%s" % (fileIdx, totalFiles, outFilePath))
            text_file.write(text) 
            
        fileIdx = fileIdx+1
          
    
    print("all done!")

def list_files(source):
    matches = []
    for root, dirnames, filenames in os.walk(source):
        for filename in filenames:
            if filename.lower().endswith(('.jpg')):
                matches.append(os.path.join(root, filename))
    return matches
    
def ocr_routine_example_1(img):
    image = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    retval, threshold = cv2.threshold(image,127,255,cv2.THRESH_BINARY)
    text = pytesseract.image_to_string(threshold)
  
    return text
 
        
def ocr_routine_example_2(img):
    # Preprocessing the image starts
    
    # Convert the image to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      
    # Performing OTSU threshold
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
      
    # Specify structure shape and kernel size. 
    # Kernel size increases or decreases the area 
    # of the rectangle to be detected.
    # A smaller value like (10, 10) will detect 
    # each word instead of a sentence.
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
      
    # Appplying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
      
    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, 
                                                     cv2.CHAIN_APPROX_NONE)
      
    # Creating a copy of image
    im2 = img.copy()
      
    # A text file is created and flushed
    file = open("recognized.txt", "w+")
    file.write("")
    file.close()
      
    # Looping through the identified contours
    # Then rectangular part is cropped and passed on
    # to pytesseract for extracting text from it
    # Extracted text is then written into the text file
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
          
        # Drawing a rectangle on copied image
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
          
        # Cropping the text block for giving input to OCR
        cropped = im2[y:y + h, x:x + w]
          
        # Open the file in append mode
        file = open("recognized.txt", "a")
          
        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped)
          
        # Appending the text into file
        file.write(text)
        file.write("\n")
          
        # Close the file
        file.close    
    


if __name__ == "__main__":
    main()
    
