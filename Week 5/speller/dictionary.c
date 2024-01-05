// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <strings.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include "dictionary.h"

// Rest of your code...
// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;
int countWord =0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Hash word to obtain a hash value
    int hashNum = hash(word);

    // Traverse the linked list at this index
    for (node *n = table[hashNum]; n != NULL; n = n->next)
    {
        // If word is found, return true
        if (strcasecmp(word, n->word) == 0)
        {
            return true;
        }
    }

    // Word not found
    return false;
}
// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    unsigned int length = 0;
    unsigned int ascii_sum = 0;
    for (int i = 0; word[i] != '\0'; i++) {
        length++;
        ascii_sum += tolower(word[i]);
    }
    unsigned int hash_value = length * ascii_sum * 31;
    return hash_value % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    FILE *infile = fopen(dictionary, "r");
    if (infile == NULL) {
        return false;
    }
    char str[LENGTH + 1];
    while (fscanf(infile, "%s", str) != EOF) {
        node *new = malloc(sizeof(node));
        if (new == NULL) {
            return false;
        }
        strcpy(new->word, str);

        int hashNum = hash(str);

        if (table[hashNum] == NULL) {
            new->next = NULL;
        } else {
            new->next = table[hashNum];
        }
        table[hashNum] = new;
        countWord += 1;
    }
    fclose(infile);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return countWord;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++) {
        while (table[i] != NULL) {
            node *temp = table[i]->next;
            free(table[i]);
            table[i] = temp;
        }
    }
    return true;
}
