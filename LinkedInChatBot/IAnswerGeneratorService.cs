namespace LinkedInChatBot
{
    public interface IAnswerGeneratorService
    {
        Task<string> GenerateAnswer(string prompt);
    }
}
