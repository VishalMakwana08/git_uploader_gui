# git_uploader_gui
This GitHub Repository Manager is a user-friendly desktop application built with Python and Tkinter. It provides a simple graphical interface (GUI) for performing two common Git operations: 1. Cloning a Repository and 2. Uploading a File
# GitHub Repository Manager GUI

A simple desktop application built with Python and Tkinter to clone GitHub repositories and upload files with ease. This tool provides a graphical user interface for common Git operations, making it accessible for those who prefer not to use the command line.

*(A screenshot of the application running would be ideal here)*
![App Screenshot](screenshot.png) 

## Features

- **Clone Repositories**: Clone any public or private GitHub repository to a local folder.
- **Upload Files**: Easily select a file, and the app will automatically copy, stage, commit, and push it to your remote repository.
- **PAT Support**: Authenticate with private repositories using a GitHub Personal Access Token for enhanced security.
- **Responsive UI**: The application uses threading to perform Git operations in the background, so the user interface never freezes.
- **Real-time Feedback**: A status log provides detailed, timestamped updates on all operations.
- **Progress Indicator**: A progress bar shows the status of the file upload process.
- **Directory Validation**: The app checks if the target directory for cloning is empty to prevent errors.

## Prerequisites

Before you run this application, you need to have the following installed on your system:

1.  **Python 3.x**
2.  **Git**: The application relies on the Git command-line tool being installed and accessible in your system's PATH. You can download it from [git-scm.com](https://git-scm.com/).
3.  **Python Libraries**: You will need the `GitPython` library. You can install it using pip:
    ```sh
    pip install GitPython
    ```
    *Note: `tkinter` is usually included with Python, but on some Linux distributions, you may need to install it separately (e.g., `sudo apt-get install python3-tk`).*

## How to Use

Here are the steps to use the application, formatted with HTML for clarity.

<br>

<details>
  <summary><strong>Click here to see the steps</strong></summary>
  
  <ol>
    <li>
      <strong>Run the Application</strong>
      <ul>
        <li>Save the code as <code>git_uploader_gui.py</code>.</li>
        <li>Open your terminal or command prompt, navigate to the directory where you saved the file, and run it:</li>
      </ul>
      <pre><code>python git_uploader_gui.py</code></pre>
    </li>
    <br>
    <li>
      <strong>Step 1: Clone a Repository</strong> (Only needed the first time)
      <ul>
        <li>In the <strong>GitHub Repository URL</strong> field, paste the full URL of the repository you want to clone (e.g., <code>https://github.com/your-username/your-repo.git</code>).</li>
        <li>If your repository is private, you must provide a <strong>GitHub Personal Access Token (PAT)</strong>. <a href="https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens">Learn how to create one here</a>.</li>
        <li>Click the <strong>Browse...</strong> button next to <strong>Local Repository Path</strong> to select an <em>empty</em> folder on your computer where the repository will be stored.</li>
        <li>Click the <strong>Clone Repository</strong> button. The status log at the bottom will show the progress.</li>
        <li>If the local directory already contains the repository, the cloning step will be skipped.</li>
      </ul>
    </li>
    <br>
    <li>
      <strong>Step 2: Upload a File</strong>
      <ul>
        <li>Ensure the <strong>Local Repository Path</strong> field points to your cloned repository.</li>
        <li>Click the <strong>Browse...</strong> button next to <strong>Select File to Upload</strong> and choose the file you want to add to the repository.</li>
        <li>Click the <strong>Upload File to Repository</strong> button.</li>
        <li>The application will:
          <ol type="a">
            <li>Copy the selected file into the local repository folder.</li>
            <li>Add the file to the Git staging area (<code>git add</code>).</li>
            <li>Commit the file with a message like "Add filename.ext via GitHub Uploader GUI" (<code>git commit</code>).</li>
            <li>Push the changes to your remote GitHub repository (<code>git push</code>).</li>
          </ol>
        </li>
        <li>Watch the progress bar and status log for real-time updates. A success message will pop up when the process is complete.</li>
      </ul>
    </li>
  </ol>
</details>

## Important Notes

- **Personal Access Token (PAT)**: Using a PAT is the recommended way to authenticate with GitHub for automated tools. Treat your token like a password and do not share it publicly. When creating a token, ensure you give it the `repo` scope to allow it to access and write to your repositories.
- **Error Handling**: If a Git command fails, a detailed error message will appear in a pop-up window and in the status log. This often happens due to incorrect URLs, invalid tokens, or merge conflicts.

## License

This project is licensed under the MIT License.
