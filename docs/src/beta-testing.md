# Beta Testing

## Testing scenarios

- Case A: The game is fully functional - i.e., frontend and backend are implemented and communicate correctly. In this case, the testing is performed on the frontend by playing the game.
- Case B: The game is partially functional - i.e., frontend is not fully connected to the backend. In this case, the testing is performed on the backend by sending requests to the API endpoints using the `api/v1/*/` endpoints or `docs/` url.
- Case C: The backend is partially functional - i.e., the backend is not fully implemented. In this case, the testers will interview the developers about what is working and what is not, and about the main issues they encountered and discuss/advise on how to fix them.

## Group Information

- Your group and team members:
  - Group: C01
  - Team members: Eric Rubio Poch, David Madrid Leon

## Tested Group Information

### Test group 1

- Test group 1:
  - Group: C02
  - Team members: [Member 1, Member 2]

### Case A checklist

- Initialization:
  - [x] authentication works correctly
  - [x] (**OPT**) registration is implemented
  - [x] game can be created
- Gameplay:
  - [x] can place ships
  - [x] can fire shots
  - [x] can receive hits and misses
  - [x] can play against a bot
  - [x] game ends correctly (win/loss)
  - [x] (**OPT**) multiplayer is implemented
  - [no] multiplayer works correctly
- Stress Testing:
  - [x] can handle multiple concurrent games
  - [x] can handle multiple concurrent players
  - [no] game can be restarted (disconnected players can rejoin)
  - [x] behaviour when cookies are disabled
- Post game:

  - [no] (**OPT**) leaderboard is implemented

- Additional tests (please specify):

For group C2, the only issue we observed is that when a player wins, the game ends correctly, but a "Game Over" message is still displayed. They told us this only happens with non-admin users — admin users see the correct message — and they showed us proof, which confirms it's true.

They do not use cookies since they rely on tokens for authentication, which is working correctly.

However, when a user who already had an ongoing game logs in again, a new game is created instead of continuing the existing one.



### Test group 2

- Test group 1:
  - Group: C03
  - Team members: [Member 1, Member 2]


### Case B checklist

- Initialization:
  - [x] you can get a token pair
  - [x] (**OPT**) registration is implemented
  - [x] authorization is set up correctly for the Users API
  - [x] game can be created
- Gameplay:
  - [x] can place ships
  - [x] can fire shots
  - [x] can receive hits and misses
  - [x] can play against a bot
  - [x] game ends correctly (win/loss)
  - [] (**OPT**) multiplayer is implemented
  - [] multiplayer works correctly
- Post game:

  - [] (**OPT**) leaderboard is implemented

- Additional tests (please specify):

For group C3, the winner field is correctly updated, and the game state works as expected. However, the main issue lies in the backend: the boards and shots are not being updated properly. Everything else seems to work correctly, but the backend fails to reflect the changes on the game board and the shots made during gameplay.
