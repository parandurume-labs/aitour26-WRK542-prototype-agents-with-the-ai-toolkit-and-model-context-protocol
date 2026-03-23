# Migrate to Code

In this section, you will learn how to migrate the agent you've created in AI Toolkit to a code-based workflow.

The AI Toolkit provides generated code for agents created in Agent Builder. You can choose your preferred SDK as well as programming language. Once you have your code file, you can integrate your agent into your own app.

## Step 1: Generate the Code

In Agent Builder, click on the **View Code** button at the top right corner of the interface.

![View code button.](../../img/view-code.png)

> [!NOTE]
> Make sure you have saved your agent locally, as described in the previous section, otherwise you won't be able to see the **View Code** option.

When prompted, select your preferred client SDK (e.g. *Microsoft Agent Framework*) and programming language (e.g. *Python*). Once the new file is created, save the file to your workspace (under 'src/cora-app.py').

## Step 2: View the Code

Before running the script, review the content of the file as there may be placeholders that must be modified before running. If you need assistance understanding the script logic, you could leverage GitHub Copilot Chat in **Ask** mode.

To access GitHub Copilot Chat, select the **Toggle Chat** icon at the top of the Visual Studio Code window.

![Toggle chat button.](../../img/toggle-chat.png)

Save the generated code file to your workspace as 'src/cora-app.py'. Be sure to have the file active so that GitHub Copilot Chat can use the file as context. Alternatively, you could reference the specific file itself in your prompt to GitHub Copilot Chat.

![GitHub Copilot Chat in Ask mode.](../../img/ghcp-ask-mode.png)

> [!NOTE]
> If you see a '+' icon besides the file name, that means cora-app.py is suggested as context by GitHub Copilot Chat, but it's not yet added. Click on the '+' icon to add the file as context.
>
> ![Suggested file as context](../../img/suggested_file_context.png)

For example try the following prompt:

```
Explain what's happening in this script.
```

If there's any changes that need to be made, you could switch to **Agent** mode and request the changes to be made. You'll be requested to approve any file changes prior to committing the file updates to the script.

## (Optional) Bonus

If you'd like to run the code, save the file and follow the comments at the top of the code file. The instructions will vary as it's dependent on the client SDK and language selected.

For example, if you selected the **Microsoft Agent Framework** SDK with **Python**, follow the instructions below:

1. In the cora-app.py file, locate the section where the MCP servers are configured and verify that the URLs and ports match those of your locally running MCP servers. 

2. Update the MCP Server URLs, there are two of them, you must remove the trailing `/` so that the format is `http://localhost:PORT_NUMBER/mcp`.

    ![MCP Server URL fix](../../img/mcp_url_fix.png)

3. Open a new terminal in Visual Studio Code by selecting **Terminal** -> **New Terminal** from the top menu.

4. Install the required dependencies by using:

```
pip install --no-deps agent-framework==1.0.0rc3 agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

4. Authenticate to Azure:

```
az login
```

You'll be prompted to open a browser window and fill in a code to complete the authentication. Once back in the terminal, press **Enter** to confirm the Azure subscription selection.

5. Navigate to the directory where the code file is saved:

```
cd src
```
6. Run the script using:

```
python cora-app.py
```

> [!TIP]
> You might want to customize the user inputs to the agent in the script to test out different scenarios and see how the agent performs. Locate the 'USER_INPUTS' array definition in the script and modify the input values as needed. For example:
```
USER_INPUTS = [
    "What are the top 5 best-selling products in the last month?",
    "Which stores have low stock on circuit breakers right now?"
]
```

> [!NOTE]
> Make sure the MCP servers are running before executing the script. If you followed the previous sections of the lab, the MCP servers should already be running locally on your machine.

Consider using GitHub Copilot Chat in Agent mode to assist with creating files for the Cora agent's UI. You could also ask GitHub Copilot Chat in Agent mode to integrate the agent script into the app UI so that you'll have a working prototype of the agent!

## Key Takeaways

- Agent Builder automatically generates code for agents in multiple programming languages and SDKs, facilitating easy migration from prototype to production.
- Code files may contain placeholders that need modification before execution, requiring developers to understand and adapt the generated logic for their specific needs.
- Using GitHub Copilot Chat in Ask and Agent modes helps developers understand generated code and create additional components like UI elements for complete agent applications.

Click **Next** to proceed to the following section of the lab.
