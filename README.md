Hi everyone... We hope you’re doing ok and staying safe during these difficult times…

During ‘Lock-down’ the team at South West London TV created a free web app you can use on your computer or smart phone which we hope will get some community spirit going and make it easy for local people to help each other.

It’s called What Goes Around Comes Around (WGACA) and it’s a tool for sharing and swapping food and drink, household goods, and over-the-counter medicines with those in need. You can post a Request to let people know you need urgent help; You can post Offers of surplus items you’re able to share; and you can volunteer as a Runner to pick up nearby Offers and deliver them where they’re most needed locally.

It’s early days and we’re already working on a load of improvements to the app (mainly to protect against scammers and selfish misuse), but we wanted to start sharing it ASAP so that trusted people in the area can start helping each other.

If it proves popular, my intention is to make the app and the data available to other charities (e.g. food banks), community groups, emergency services and other agencies who are better placed to manage logistics/distribution using the tool.

TECHNOLOGY STACK

• Python 3.7 - because it’s all I know and I’m planning to have to make this happen on my own if necessary.

• https://anvil.works/ - because I don’t have time to learn and deploy a scalable web app with database, user authentication, email, and (nice to have) google maps integration and this seems like a fast route to getting something “out there” quickly.

That’s all - as few layers/dependencies as possible.

FYI I did consider setting up a simple discussion forum where people could interact with their offers/requests and may still do so for the social aspects of this but believe an app is better because the data can them be standardised, both for sharing with other charities/volunteers/government support teams and for down-stream automation (e.g. calculating optimum pick-up and drop-off delivery routes for volunteer drivers/walkers).

KEY RISKS / KNOWN INFORMATION GAPS

Abuse of the system by selfish/criminal elements. I’m thinking about making each registered user’s “karma history” available for other registered users to view - including everything they’ve offered/donated, every delivery they offered/donated, “reviewers’ comments” and on the flip side everything they’ve asked for/received. Perhaps create a moderator role blocking/blacklisting abusers. Perhaps a human/physical authentication factor such as hand delivering invitation codes to real neighbours telling them about the app; perhaps cross-checking with the UK electoral roll.
Taxonomy of objects. I can see non-standardisation becoming a problem (“toothpaste”, “tooth-paste”, “Tooth Paste”) and would appreciate any pointers towards supermarket style solutions or databases which may have already solved this problem. I think we can completely disregard brands but if there was an item/category heirarchy I could just pick up and present to users e.g. “Health & Hygeine | Dental | Toothpaste (child/adult/denture etc)” that would save a tonne of time.
Without reaching out to the like of NextDoor.co.uk who already have a solution to this, it would also be a great time saver to find an existing database that breaks down streets to towns/boroughs and possibly postcodes, or at least estimated and limited walking/driving distance in order to define “local” areas and groups.
Best wishes, peter@southwestlondon.tv
