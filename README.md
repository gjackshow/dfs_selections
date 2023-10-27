# Daily Fantasy Sports Roster Optimizer

Welcome to the Daily Fantasy Sports Roster Optimizer project! 

My goal is to help you win money by leveraging the power of machine learning algorithms to create optimized rosters for large-format competitive Daily Fantasy Sports contests. 

## The DFS Landscape
Large multi-entry tournaments attract hundreds of thousands of entries with multi-million dollar prize pools. The prizes are heavily weighted. The top score of the week might take home $1MM on a $20 bet while a score in the 20-25th percentile just doubles their investment. The bottom 75% go home with nothing.  

There are 50/50 games where it's easier to win, but there's no extra reward for coming in 1st instead of 10th in a 20 player pool. First place and tenth place both double their money. Players might use a different strategy here. Where you might pick a player with high-upside and predicted low ownership in a large tournament, here you can probably get away with playing the best points-per-salary players you can find. 

In my experience, regardless of which type of competition you're playing in, a computationally assisted person will be better at finding value.

Daily fantasy sports is a game of computational skill. [The data speaks for itself](https://www.draftkings.com/average-results). With 5% of players consistently taking home ~50% of the total prize pool on just 30% of the total bets, it's clear that some players have found an edge.

## How It's Done

My ML algorithm carefully analyzes the pool of available players and strategically assembles thousands of high-performing rosters while adhering to the salary cap.

The user can choose to influence the algorithm's automated choices by prioritizing certain players or "stacking" certain players, e.g. the QB and a WR from the same team. Or just select a few players you know in your gut are going to go off and let the algorithm take care of the rest!

The "Classic" format, which is commonly used in NFL DFS contests, includes the following 9 positions:

- 1 Quarterback (QB)
- 3 Wide Receivers (WR)
- 2 Running Backs (RB)
- 1 Tight End (TE)
- 1 Flex (can be either a RB, WR, or TE)
- 1 Defense/Special Teams (D/ST)

The algorithm is optimized for this format but can be easily extended to other DFS formats.

## Features

- Data scraping and modeling of NFL player projections from 4 sources
- Remove or "force include" players in case of injury or what your gut is telling you
- Data-driven roster optimization and ranking
- Outputs hundreds of eligible rosters for even the largest multi-entry games
- Choose how your rosters are ranked, e.g. high-risk and high-reward, or choose the "chalk" for 50/50 matchups 
- Automated settings for NFL Classic contests on Draft Kings and Yahoo
- See your rosters in the "Projections" vs "Salary" space relative to other eligible players
- Understand your exposure to individual players in multi-entry contests through visualization
- Track your account performance over its history

Up your Daily Fantasy Sports game and make informed decisions with our cutting-edge roster optimization tool. 

## How to Get Started

[Check out the visualization tools showing selected rosters for 2023 week 7 Yahoo matchups](https://gjselections.azurewebsites.net)

[And my real-world performance using the tool for the 2023 season](https://gjackshowdfs.azurewebsites.net)

## Contributors
Reach out to me if you're interested in the algorithmic DFS space and you'd like to share ideas. I have omitted the algorithm from the code so I don't have to play against "myself" but would be happy to discuss generally how it works and areas for improvement.
