namespace LinkedInChatBot
{
    class Program
    {
        static void Main(string[] args)
        {
            Assistant assistant = new();
            AnswerGeneratorHelper answerGeneratorHelper = new(assistant);

            while (true)
            {
                assistant.Prompt = Console.ReadLine();
                answerGeneratorHelper.Generate(assistant.Prompt);

                Console.WriteLine(assistant.Answer);
            }
        }
    }
}