# 💡 Data Communications Programming Assignment - Fall 2023

## Server-Client Random Calculation Matching Game Implementation

### 🚀Due Date
- Submissions must be made via eCampus by **October 12th, 23:59**.

### 🚀Submission Format
- Submit one file named `G<group_number>HW1.zip` (e.g., G1HW1.zip).

### 🚀Simulation Environment and Components
- Implement the experimental environment consisting of 4 clients and 1 server.
- The server maintains, updates, and runs a System Clock (incrementing every second).
- Upon each client connection, the server automatically issues a random arithmetic problem (two operations, no parentheses) based on integers ranging from 0 to 100.
- The server checks the client's response, sends back the result, reissues the problem if incorrect, or provides a new problem after a random time if correct.
- The server accumulates all client results, calculates the SUM, and outputs the final total before termination.
- All communications must be implemented through Sockets, and the server must be hosted externally (e.g., AWS, Google Cloud).

### 🚀Simulation Scenario
- Log all events in `Client1.txt`, `Client2.txt`, `Client3.txt`, `Client4.txt`, and `Server.txt`.
- Clients connect at random times, receive problems, compute and send back results.
- Assume no delay other than the computation time.
- The program runs for 10 minutes, after which all connections are terminated gracefully, and a total SUM is calculated and logged.

### 🚀Submission Details
- All source files and log files must be submitted in the `G<group_number>HW1.zip` package.
- Include a `Readme.txt` with:
  - Group name and all members' student IDs & names.
  - Specified roles for each student.
  - Explanation of program components.
  - Compilation method for the source code.
  - Program's runtime environment and execution method.
  - Handling of errors or additional messages.
  - Additional comments related to the assignment submission.

### 🚀Video Explanation
- Create a 5-minute video explaining the assignment.
- Submit a `download.txt` file containing a link to download the video.
- Ensure the video is accessible and playable, as failure to do so will result in penalties.

By following this README structure, your assignment submission will be organized and compliant with the given instructions.
