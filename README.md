# File Classification with LLM APIs

## Summary

This project classifies files through parsing and leveraging Perplexity LLM API. The building blocks are:
- A Flask API endpoint to trigger classification
- PDF and Image parsing via OCR
- Sending parsed text to Perplexity LLM API to get one of the available classifications
- Alternative classification based on provided filename using `nltk` and `tokenization`

### How to run

1. Create `.env` file with the Perplexity token.
   ```
   PERPLEXITY_API_TOKEN=<token>
   ```

#### With Virtualenv

2. Install additional dependencies: `tesseract`, `popplar`
   ```
   brew install tesseract
   brew install popplar
   ```

3. Continue with virtualenv instructions below, install requirements.txt and then run server.

#### With Docker

**WARNING:** If you try to hit the endpoint with a browser on Mac, using `localhost:5000` will not work but `127.0.0.1:5000` will. For curl, bot should be fine. See this [Stackoverflow issue](https://stackoverflow.com/questions/72795799/how-to-solve-403-error-with-flask-in-python) for more details.

1. `docker-compose build`

2. `docker-compose up`

### Testing

Please note that the default files are now in `files/raw` folder.

Some unit tests are provided in the `tests` folder and can be run with `python -m pytest`.

1. Test the classifier using a tool like curl:
    ```shell
    curl -X POST -F 'file=@files/raw/bank_statement/bank_statement_1.pdf' http://127.0.0.1:5000/classify_file
    ```

2. You can explicitly set the classifier to `classifier=content_classifier` (default) or `classifier=filename_classifier`
    ```shell
    curl -X POST -F 'file=@files/raw/bank_statement/bank_statement_1.pdf' "http://127.0.0.1:5000/classify_file?classifier=filename_classifier"
    ```

3. You can also set `convert_pdf_to_image=true` to convert PDFs to images first, which gives more accurate output for poorly formatted PDFs:
    ```shell
    curl -X POST -F 'file=@files/raw/bank_statement/bank_statement_1.pdf' "http://127.0.0.1:5000/classify_file?convert_pdf_to_image=true"
    ```


### Future Improvements

- Arguably, an LLM is not the best tool for this task. If we continue with LLMs, we could run TinyLLama locally and use that instead of Perplexity. This would solve the issue of sending private information to a third party. We might want to make this its own microservice to improve performance due to cold-start.
- We could also improve the prompt and fine-tune the configuration to ensure we only get the category back (and not additional text).
- More testing data needs to be gathered to evaluate the accuracy of the model and identify its weaknesses.
- With a bit more time and a realistic dataset, we could train our own classifier via LogisticRegression, which would be more efficient than an LLM.
