namespace LinkedInChatBot
{
    public class AnswerGeneratorHelper
    {
        AnswerGeneratorService answerGeneratorService = new();
        List<string> answers = new();
        Assistant assistant;

        public AnswerGeneratorHelper(Assistant assistant)
        {
            this.assistant = assistant;
        }

        public async void Generate(string? prompt)
        {
            if (!string.IsNullOrEmpty(prompt))
            {
                var answer = await answerGeneratorService.GenerateAnswer(prompt);
                answers.Add(answer);

                assistant.Answer = answers.ToString();
            }
        }
    }
}
