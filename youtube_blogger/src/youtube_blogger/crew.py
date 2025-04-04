from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
load_dotenv()

@CrewBase
class YoutubeBlogger():
    """YoutubeBlogger crew"""

    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    
    @agent
    def summarizer(self) -> Agent:
        return Agent(
            config=self.agents_config['summarizer'],
            verbose=True
        )

    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config['writer'],
            verbose=True
        )

    @task
    def task_summarize(self) -> Task:
        return Task(
            config=self.tasks_config['task_summarize'],
        )

    @task
    def task_write(self) -> Task:
        return Task(
            config=self.tasks_config['task_write'],
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the YoutubeBlogger crew"""
        

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
