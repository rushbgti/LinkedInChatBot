using OpenAI_API;
using OpenAI_API.Completions;

namespace LinkedInChatBot
{
    public class AnswerGeneratorService : IAnswerGeneratorService
    {
        public async Task<string> GenerateAnswer(string prompt)
        {
            string apiKey = "";
            string answer = string.Empty;

            var openAi = new OpenAIAPI(apiKey);
            CompletionRequest completion = new CompletionRequest();
            completion.Prompt = prompt;
            completion.MaxTokens = 4000;
            var result = await openAi.Completions.CreateCompletionAsync(completion);
            if (result != null)
            {
                foreach (var item in result.Completions)
                {
                    answer = item.Text;
                }
            }

            return answer;
        }
    }
}
