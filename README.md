# HatTrick House

## Team Members:
- **Joan Cerdà**
- **Joan Barber**
- **Armando Diaconu**
- **Unai Celaya**
- **Rossend Prats**

## Project Overview

We are building a **Sports Betting Platform** that integrates real-time data from various sports leagues through APIs. The website will provide live odds, match updates, and betting opportunities, offering users an engaging and user-friendly experience. This platform will cover a wide range of sports like football, basketball, and tennis.

### Key Features:
- **Real-time API Integration**: Fetches live data from sports leagues (e.g., football, basketball, tennis) for up-to-date match results and odds.
- **User Interface**: A simple, intuitive design that allows users to browse events, place bets, and track results easily.
- **Betting System**: A secure and responsive system for placing live bets with notifications on odds changes and results.
- **Analytics & Statistics**: Detailed insights and stats to help users make informed betting decisions based on historical performance and trends.

## Topic: Sports Betting Platform

## Entities: Users – Sports – Leagues – Teams – Matches – Bets – Odds

The system manages live sports betting with real-time data integration.

-**One Sport → many Leagues (1-N)**
-**One League → many Teams (1-N)**
-**Teams ↔ Matches (N-M, teams play many matches; each match involves teams)**
-**One Match → many Odds updates (1-N)**
-**One User → many Bets (1-N)**
-**Users ↔ Matches (N-M through Bets)**
