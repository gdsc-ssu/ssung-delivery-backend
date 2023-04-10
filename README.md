## 🛠️ Technology & Architecture

Our team chose FastAPI as the backend framework for our project due to its ease of use in building APIs and its support
for asynchronous processing, allowing for efficient backend system development. Additionally, FastAPI is written in
Python, which provides advantages in code reproducibility and development speed. We also utilized Docker containers for
easy environment management and Cloud Run for quick deployment. For our relational database needs, we chose to use
Google Cloud SQL, which allowed us to leverage its features such as automated backups and scalability. Finally, we used
various GCP services such as Cloud Build and Artifact Registry for streamlined container image management.

| Tech Spec | Description                                                                                                                                                                                                                                       |
|-----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Cloud Run | <ul><li>Fast deployment</li><li>Easy environment management through Docker</li><li>Built-in CI/CD features</li><li>Serverless architecture to reduce server costs</li><li>Use Artifact Registry for Docker image storage and versioning</li></ul> |
| Cloud SQL | <ul><li>Delivery data has a predefined schema.</li><li>Best option for managing data in a structured manner in the GCP environment.</li></ul>                                                                                                     |
| FastAPI   | <ul><li>Easiest framework for building APIs</li><li>Provides efficient backend system construction with asynchronous processing logic</li><li>Utilizes Python, enabling code reproducibility and fast development speed</li></ul>                 |

## 🔑 Key Implementations

### Word Identifer

Word identifiers refer to the ability to identify information by a specific combination of words instead of identifiers
in the form of serial numbers. For example, you can identify shipping information by a combination of words such as "
nice, clock, day" instead of the serial number "abjxk124ba7". This makes word combinations more intuitive, easier to
understand, and easier to remember identifiers than serial numbers. In addition, word identifiers are more secure and
can be useful in services that handle information that is important to security.

### Work Flow

### Flow

- Create
    1. The user registers the shipping information.
    2. The server randomly extracts 3 words from the word DB.
    3. Combine the 3 extracted words into one string.
    4. Encodes the combined string into Base64.
    5. Run a duplicate check to see if the encoded string already exists in the DB.
    6. If not duplicated, store the encoded string in the DB with the shipping information.
    7. Repeat steps 2 through 5 if duplicated.
- Read
    1. The user enters a word identifier.
    2. The encoder inside the service encodes the user-entered word identifier into Base64.
    3. Get the order information by sending a query to the DB with the encoded value.
    4. Show the imported order information to the user.

## 📌 Going Forward

We will introduce golang and gRPC additionally.

- [ ]  golang - Enable efficient and reliable programming language
- [ ]  gRPC - Enables rapid data transfer and scalable service development