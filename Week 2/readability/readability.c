#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

float count_letters(string text, int str_length);
float count_words(string text, int str_length);
float count_sens(string text, int str_length);

int main(void)
{
    // Prompt user for text
    string text = get_string("Text: ");

    // Find length of text
    int length = strlen(text);

    // Find the number of letters in text
    float letter_count = count_letters(text, length);

    // Find the number of words in text
    float word_count = count_words(text, length);

    // Find the number of sentances in text
    int sen_count = count_sens(text, length);

    // Calculate the average number of letters and sentances per 100 words
    int L = round((100 / word_count) * letter_count);
    int S = round((100 / word_count) * sen_count);

    // Calculate and show grade level
    float index = 0.0588 * L - 0.296 * S - 15.8;
    index = round(index);

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 0 && index < 16)
    {
        printf("Grade %i\n", (int) index);
    }
    else
    {
        printf("Grade 16+\n");
    }
}

float count_letters(string text, int str_length)
{
    int letters = 0;

    // Checks every character
    for (int i = 0; i < str_length; i++)
    {
        // Checks if it is a letter
        if (isalpha(text[i]) != 0)
        {
            // If true, add one to number of letters
            letters++;
        }
    }
    // Returns the number of letters
    return letters;
}

float count_words(string text, int str_length)
{
    int words = 0;

    // Checks every character
    for (int i = 0; i < str_length; i++)
    {
        // Checks for a space
        if (text[i] == 32)
        {
            // If true, Add one to number of words
            words++;
        }
    }
    // Adds word from the end of text
    words++;

    // Returns the number of words
    return words;
}

float count_sens(string text, int str_length)
{
    int sentences = 0;

    // Checks each character
    for (int i = 0; i < str_length; i++)
    {
        // Checks for end of sentance
        if (text[i] == '!' || text[i] == '.' || text[i] == '?')
        {
            // If true, add one to the number of sentences
            sentences++;
        }
    }
    // Returns number of sentences
    return sentences;
}