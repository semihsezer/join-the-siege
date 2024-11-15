# Heron Coding Challenge - File Classifier

## Summary

Hello, thanks for taking the time to review my assignment. I focused on achieving decent accuracy with the limited time.

I improved the FilenameClassifier to use `nltk`, `tokenization` and autocorrect to help with spelling mistakes. It takes a second or two to run.

I also added a `FileContentClassifier`. The parsed text from PDFs seemed to have accuracy issues, so I did not go the synthetic data route. I experimented with different PDF modules and configurations to get more accuracy with PDF parsing. I also added an option to convert PDFs to an image first, and then doing OCR on it. This is a lot more more accurate with poorly formatted PDFs, but it comes with a performance sacrifice (takes 1 or 2 seconds). You can see `files_extracted` folder to see my parsed text for each provided file using each parser.

I am a bit rusty on training models from scratch and struggled to find datasets with comparable PDFs. This made me choose an online LLM (Perplexity) for the simplicity and I send it a limited text extract from the documents. I ask it to classify the extract into one of the 4 predefined categories (bank_statement, drivers_license, invoice, other). To prevent hallucinations, I require it to strictly return the category name only, otherwise it is a failed classification. Admittedly, it sometimes doesn't return me just the category and instead returns a sentence.

The disadvantage of this appraoch is cost, performance sacrifice and sending private information to a third party. Cost and performance sacrifice might be acceptable for an MVP, but private information may not.


### How to run

1. Create `.env` file with the Perplexity token. I submitted this together with the link to my repo (I am aware this is not a secure way to share it but it is the easiest for now and it is just a temporary token.)
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

**WARNING:** Docker setup is not complete as I wasn't able to expose `0.0.0.0` from inside the container. I have done this many times for apps like Django and FastAPI but for some reason this didn't work today, either due me not knowing the specifics of Flask or a networking issue on my machine. I spent more time on it than I would like to admit so I hope this is OK.

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


### Production Considerations
- Dockerize and deploy to cloud with a load balancer, where server instances and workers can be auto scaled easily.
- Run the server with `asgi` or `uvicorn` to handle concurrent requests with multiple processes and instances
- Use background workers and a job queue (like Celery or Airflow) to separate file processing
  - Return a `file_id` to the client and ask it to check it periodically
- Use object storage like S3 to store uploaded files, also add a `/upload-file` endpoint
- Check the actual file mime type rather than just looking at the extension (ie. having `.pdf` in the filename doesn't mean that it is actually a pdf)
- Disable certain file types for security (ie. `.exe` files etc.)
- Use a database (PostgreSQL) to store processed files
- Generate a `sha` for each file and if the exact same file is submitted do not reclassify (unless we change the model)
- Store prediction metadata in the DB to monitor model performance (ie. model version, prediction, success/failure, error messages, duration, etc.)


## Overview

At Heron, we’re using AI to automate document processing workflows in financial services and beyond. Each day, we handle over 100,000 documents that need to be quickly identified and categorised before we can kick off the automations.

This repository provides a basic endpoint for classifying files by their filenames. However, the current classifier has limitations when it comes to handling poorly named files, processing larger volumes, and adapting to new industries effectively.

**Your task**: improve this classifier by adding features and optimisations to handle (1) poorly named files, (2) scaling to new industries, and (3) processing larger volumes of documents.

This is a real-world challenge that allows you to demonstrate your approach to building innovative and scalable AI solutions. We’re excited to see what you come up with! Feel free to take it in any direction you like, but we suggest:


### Part 1: Enhancing the Classifier

- What are the limitations in the current classifier that's stopping it from scaling?
- How might you extend the classifier with additional technologies, capabilities, or features?


### Part 2: Productionising the Classifier

- How can you ensure the classifier is robust and reliable in a production environment?
- How can you deploy the classifier to make it accessible to other services and users?

We encourage you to be creative! Feel free to use any libraries, tools, services, models or frameworks of your choice

### Possible Ideas / Suggestions
- Train a classifier to categorize files based on the text content of a file
- Generate synthetic data to train the classifier on documents from different industries
- Detect file type and handle other file formats (e.g., Word, Excel)
- Set up a CI/CD pipeline for automatic testing and deployment
- Refactor the codebase to make it more maintainable and scalable

## Marking Criteria
- **Functionality**: Does the classifier work as expected?
- **Scalability**: Can the classifier scale to new industries and higher volumes?
- **Maintainability**: Is the codebase well-structured and easy to maintain?
- **Creativity**: Are there any innovative or creative solutions to the problem?
- **Testing**: Are there tests to validate the service's functionality?
- **Deployment**: Is the classifier ready for deployment in a production environment?

## Pre-Requisites
1. Python 3.12
2. Install `pre-commit`
3. Install `tesseract`: `brew install tesseract` for extracting text from images
4. Install `poppler`: `brew install poppler` for converting PDFs to images

## Getting Started
1. Clone the repository:
    ```shell
    git clone <repository_url>
    cd heron_classifier
    ```

2. Install dependencies:
    ```shell
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. Run the Flask app:
    ```shell
    python -m src.app
    ```

4. Test the classifier using a tool like curl:
    ```shell
    curl -X POST -F 'file=@path_to_pdf.pdf' http://127.0.0.1:5000/classify_file
    ```

5. Run tests:
   ```shell
    pytest
    ```

## Submission

Please aim to spend 3 hours on this challenge.

Once completed, submit your solution by sharing a link to your forked repository. Please also provide a brief write-up of your ideas, approach, and any instructions needed to run your solution.
