from office import OfficeQuotes

season3 = OfficeQuotes(3)
random_quote = season3.random_quote()
random_quote_from_episode7 = season3.random_quote(7)
quotes_by_kevin = season3.quotes_from_character('kevin', 3)

print random_quote
print random_quote_from_episode7
print quotes_by_kevin