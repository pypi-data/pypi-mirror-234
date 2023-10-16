```
 _____ _____ _       _   _ _               ____ _     ___ 
|___ /|  ___| | __ _| |_| (_)_ __   ___   / ___| |   |_ _|
  |_ \| |_  | |/ _` | __| | | '_ \ / _ \ | |   | |    | | 
 ___) |  _| | | (_| | |_| | | | | |  __/ | |___| |___ | | 
|____/|_|   |_|\__,_|\__|_|_|_| |_|\___|  \____|_____|___|
```                                

## Quickstart

3Flatline Dixie platform is a static code analyzing platform that works on a number of different languages: C/C++. ObjC, Golang, Java, Python, Ruby, JavaScript, PHP, and decompiled pseudo-C.  It uses a number of different methods to scan your submitted code and find potential vulnerabilities.

In order to get started you will need to have valid credentials and an available number of tokens as part of your subscription.  Also, if you just received credentials created by the system when your account was registered *YOU MUST CHANGE YOUR PASSWORD USING THE WEB GUI BEFORE YOU CAN USE THE CLI*.  That can be accessed [on the website here](https://auth.3flatline.ai/login?client_id=573488kv0r42co4tv0j8qokeko&response_type=code&scope=email+openid+phone&redirect_uri=https%3A%2F%2F3flatline.ai).

## Running the CLI

The CLI will require you to log in before you create any jobs.

## Commands: 
| Action | Command Example |
| -- | -- |
|Authenticate | `authenticate -u <username> -p <password>` |
|Get user token allocation | `user` |
|Estimate token cost for file/directory | `estimate <filepath for analysis>`|
|Create a job from file/folder |`create_task <filepath for analysis>`|
|Get status of all jobs | `status`|
|Search for specific status| `status -s <task_id> <task id>...`|
|List all jobs and results you have created| `list`|
|List a specific job’s info/results| `list -s <task id> <task id>...`|
|Download results| Add flag to list `-d <output filepath>`|
|Download results as markdown| Add flag to list `-m -d <output filepath>`|
|Delete task(s)| `delete <task id> <task id>...`|

The `status` command will also output all task IDs to make it easier to use with other commands.

To run any of these commands immediately on start, string them with quotes on the command line:

```python3 3flatline-cli-cmd2.py "authenticate -u <username> -p <password>" "create_task <path>" "status"```


To create multiple jobs from the cli, quote the individual commands you would like run:

```python3 3flatline-cli-cmd2.py "authenticate -u aaron@3flatline.ai -p DefNotMyPassword!" "create_task /home/user/3flatline/cli/test_file1.c" "create_task /home/user/3flatline/cli/test_file2.c"```


Keep in mind that each run of the CLI requires authentication.  The CLI will maintain a token while it is open and will refresh your authorization before each command is run, but only if you keep the CLI open.  If the CLI is closed, you will need to reauthenticate with the server.  

## What does 3Flatline do and getting the best results

3Flatline automatically finds bugs in source code and assembly that has been decompiled to c. 3Flatline is a LLM trained on millions of different bug examples. There are 2 different models to query against. There is a model focused on bug classes for C based languages. The other model is everything else. Automatically determining the best model to run against is on our road map.

### C-Based Languages
The platform will work with any C based language. Note that 3Flatline performs well against firmware and assembly that has been decompiled to C. To have 3Flatline analyze decompiled C, be sure to remove the data section and any trampoline functions. For C like languages(golang, Rust), the best results are from running 3Flatline against the compiled code and not the source. 


### Other Languages
The platform is best used on web application source code (php, ruby etc). 

## Limitations
LLM AI platforms are limited by the number of tokens they can process. As a result, the platform is limited by the amount of context it can process. What does this mean to you? 3Flatine doesn't produce high quality results for bug classes that require a lot of context. 
For example: 
- 3Flatline doesn't understand runtime environments. Sending Rust source code can result in a number of false positives, because 3Flatline doesn't understand the memory protections of the Rust runtime. 
- The platform doesn't understand function or class definitions well. Header files and any file that serves the purpose of an interface in object oriented programing doesn't produce good results.
- It also doesn't understand the difference between a class definition and a class implementation. We still recommend having 3Flatline analyze those files. 3Flatline can identify a poorly allocated memory segment in a struct.
- In general, 3Flatline doesn't do well with highly abstracted code. We recommend running at least the preprocessor against the source code to remove some abstraction. 

3Flatline is a generative AI and as a result will have false positives. We have reduced those greatly but it can *still* happen.

## Vulnerable bugs
While 3Flatline finds bugs, it doesn't tell you if they are vulnerable. Determining the reachability of the bug is on our roadmap.

Currently, the size of the file to analyze is 18k tokens. What does that mean in english? If a file returns as too big to analyze, break it up into the largest file possible that still is under the token limit. Be sure not to chunk the file in the middle of a function. Doing this automatically is on the roadmap.

## Privacy
Code is only on the servers long enough to be scanned. You retain all rights to your code and to the results. We auto delete results after 7 days and you can delete results immediately if you desire. No human ever looks at your code. We do send the code to a private Azure OpenAI endpoint as part of our process.  Your data is not retained or used for training or fine-tuning models.

You can see the Azure OpenAI service privacy policy [here](https://learn.microsoft.com/en-us/legal/cognitive-services/openai/data-privacy)

Their claims to how they handle input are their own. If you are really concerned about privacy, compile your code, heck even strip symbols, and use the methods described above for analysis on assembly.


> McCoy "the Dixie Flatline" Pauly was a legendary console cowboy, or hacker in the book Neuromancer by William Gibson. 

> He received his nickname because his system hacks were so difficult he flatlined (read: died) during a couple of them. Dixie has been dead awhile, but his memories live on in a ROM construct, meaning Dixie can't create new memories or learn or grow in any meaningful way. The ROM construct is simply the memories and instincts of a dead man that create a feedback loop, so he "always does what [you] expect him to" (17.38). Dixie finds his inability to change a total drag and asks Case to delete him once the job is done.
