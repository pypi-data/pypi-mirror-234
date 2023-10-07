#include <string>
#include <sstream>
#include <vector>
#include <algorithm>
#include <cctype>

namespace QStringUtils{
    
    /**
     * @brief Strips leading and trailing characters from a string.
     *
     * This function removes leading and trailing characters specified in 'characters' 
     * from the input string 'str'. If no characters are specified, it defaults to stripping 
     * whitespace characters.
     *
     * @param str The input string from which leading and trailing characters are to be removed.
     * @param characters A string of characters to be considered for removal from the start and end of 'str'.
     *                   Defaults to whitespace characters if not specified.
     * @return A new string which is a copy of the input string 'str' but with leading and trailing 
     *         'characters' removed. If 'str' only contains characters from 'characters', an empty string is returned.
     */
    std::string strip(const std::string& str, const std::string& characters = " \t")
    {
        const auto strBegin = str.find_first_not_of(characters);
        if (strBegin == std::string::npos)
            return std::string();

        const auto strEnd = str.find_last_not_of(characters);
        const auto length = strEnd - strBegin + 1;

        if (strBegin == 0 && length == str.size()) {
            // If there are no leading or trailing characters to strip, return the original string
            return str;
        } else {
            // Otherwise, create a new string with the leading and trailing characters stripped
            return str.substr(strBegin, length);
        }
    }

    
    /**
     * @brief Splits a string into a vector of substrings (tokens) based on a given delimiter.
     *
     * This function breaks up a string into a vector of substrings based on a given delimiter. 
     * By default, it uses a whitespace character as the delimiter, discards empty tokens, and does not 
     * strip leading or trailing whitespace from the tokens. These behaviors can be changed using the 
     * optional arguments.
     *
     * @param str The string to split.
     * @param delimiter The character to use as the delimiter for splitting the string. Defaults to whitespace.
     * @param removeEmptyTokens If true, the function will discard empty tokens. Defaults to true.
     * @param stripWhitespace If true, the function will strip leading and trailing whitespace from the tokens. Defaults to false.
     * @return A vector of substrings (tokens) obtained by splitting the input string.
     */
    std::vector<std::string> split(const std::string &str, char delimiter = ' ', bool removeEmptyTokens = true, bool stripWhitespace = false) {
        std::vector<std::string> tokens;
        std::string token;
        std::stringstream tokenStream(str);

        while (std::getline(tokenStream, token, delimiter)) {
            if (stripWhitespace) {
                token = strip(token);
            }
            if (!removeEmptyTokens || !token.empty()) {
                tokens.push_back(token);
            }
        }

        return tokens;
    }

};

