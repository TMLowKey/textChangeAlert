# About
Simple alert system which control changes in specified field on screen and if there is change of text it make sound.
- Use case?
    - I use it check for new identification plates on my parking spot.
- Why text only?
    - I had problem with visual clutter (people, animals), tracking pixel changes did not worked.

# Usage
1. Be sure you have tesseract library.
    - for release version follow "Requirements" 
2. Run program as admin.
3. Use mouse your mouse for highlighting space you want to check. Be precise, tesseract library can be quiet finicky. 
4. For closing terminal window press Ctrl + C
If you want change sound just change `alertSound.wav` for another .wav file just dont forget it to rename it.

# Requirements
- Python3 https://www.python.org/
- Tesseract (open source text recognition engine)
    - Download for windows: https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.1.20230401.exe
        - On Windows, you may need to add the Tesseract installation directory to your system's PATH environment variable. This step is not required for macOS or Linux.
            - Search for "Environment Variables" in your Windows search bar.
            - Click on "Edit the system environment variables."
            - In the System Properties window, click the "Environment Variables" button.
            - In the "System Variables" section, find the "Path" variable and click "Edit."
            - Add the path to the Tesseract executable (usually C:\Program Files\Tesseract-OCR) to the list of paths.
        - Verify installation with `tesseract --version`

    - For Linux read githubpage https://tesseract-ocr.github.io/tessdoc/Installation.html
    
- In your command line run `pip install -r requirements.txt`