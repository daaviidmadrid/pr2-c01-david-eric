# Self Testing

## Group Information

- Your group and team members:
  - Group: C01
  - Team members: Eric Rubio Poch, David Madrid Leon
  - Date: 28-05-2025 (testing class)

### Implementation checklist

- Initialization:
  - [X] authentication works correctly
  - [X] (**OPT**) registration is implemented
  - [X] game can be created
- Gameplay:
  - [X] can place ships
  - [X] can fire shots
  - [X] can receive hits and misses
  - [X] can play against a bot
  - [] game ends correctly (win/loss)
  - [] (**OPT**) multiplayer is implemented
  - [] multiplayer works correctly
- Stress Testing:
  - [] can handle multiple concurrent games
  - [] can handle multiple concurrent players
  - [] game can be restarted (disconnected players can rejoin)
  - [] behaviour when cookies are disabled
- Post game:

  - [] (**OPT**) leaderboard is implemented



### Encountered issues, how you solved them if you did.

At the time of the testing session, we had the initial part of the backend implemented. Token-based authentication was already working correctly, and it was possible to create a game through the API. However, the backend was not yet handling game state updates.

The frontend allowed us to play the game — we could place ships, take turns, and the interface responded correctly — but none of this was being saved or tracked in the backend. Actions like firing or sinking ships were only processed on the client side, so the server didn’t store any of this information. Additionally, the game never ended from the backend’s perspective, and the winner was not set when one player had supposedly won.

### Post testing improvements

After the testing session, we focused on migrating all the game logic to the backend. We implemented persistent handling of game actions such as placing ships, firing shots, tracking hits and misses, and detecting when a game should end. The backend now stores all relevant data and responds accordingly to each user action.

We also fixed the issue where games never ended and added logic to declare a winner once all ships of a player were sunk. The API was extended to fully support backend-driven gameplay, ensuring that the game could be played entirely through validated requests.

At this point, all main features work as expected, including player authentication, ship placement, gameplay against the bot, and proper game termination. The only functionalities we have not implemented are the multiplayer mode and the post-game leaderboard, which were marked as optional.