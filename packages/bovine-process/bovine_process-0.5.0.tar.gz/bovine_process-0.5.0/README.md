# bovine_process

`bovine_process` consists of the side effect logic of Activity objects. This means it contains the code, the logic that for an incoming object, one executes:

- Store object in bovine_store
- Add reference to inbox
- Perform side effects
- Enque object for bovine_pubsub

And a similar list of effects for outgoing objects, i.e

- Store object in bovine_store
- Add reference to outbox
- Perform side effects
- Send objects to follower's inbox
- Enque object for bovine_pubsub

The behavior defined in this package corresponds to [6. Client to Server Interactions](https://www.w3.org/TR/activitypub/#client-to-server-interactions) and [7. Server to Server Interactions](https://www.w3.org/TR/activitypub/#server-to-server-interactions) of the ActivityPub specification. However, only a small subset of side effects is implemented.

## Implemented Side Effects

- Create, Update, Delete on objects, i.e. basic crud
- Like, Dislike, EmojiReact -> add to likes collection; Undo removes
- Announce -> add to share collection; Undo removes
- The same person can Like, Announce, etc.. multiple times
- Create with inReplyTo -> add to replies collection; Delete removes

- Follow and Accept
  - Outgoing Accept of Follow adds to followers
  - Incoming Accept of Follows adds to following

- [ ] Specify Update checks
- [ ] Authority checks.
- [ ] Refactor for easier customization / extension. Adding a new side effect currently requires publishing a new package. This should not be the case.

## Tests

The folder `tests/data` contains test cases what side effects happen in the database for certain cases.
