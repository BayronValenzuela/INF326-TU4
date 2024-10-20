## Project Setup

To set up and run the project using Docker Compose, follow these steps:

1. **Ensure Docker and Docker Compose are installed**:

   - Docker: [Install Docker](https://docs.docker.com/get-docker/)
   - Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

2. **Navigate to the project directory**:
   Open a terminal and change to the directory containing the `docker-compose.yaml` file:

3. **Run Docker Compose**:
   Execute the following command to start your services as defined in the `docker-compose.yaml` file:

   ```sh
   docker-compose up
   ```

4. **Optional: Run in detached mode**:
   To run the containers in the background, add the `-d` flag:

   ```sh
   docker-compose up -d
   ```

5. **Stopping the services**:
   To stop the running services, use:

   ```sh
   docker-compose down
   ```

6. **Viewing logs**:
   To view the logs of your services, use:

   ```sh
   docker-compose logs
   ```

7. **Additional commands**:
   For more Docker Compose commands, refer to the [official documentation](https://docs.docker.com/compose/reference/).
