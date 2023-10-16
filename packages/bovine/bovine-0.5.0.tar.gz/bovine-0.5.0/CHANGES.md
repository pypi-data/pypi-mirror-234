# Changes to Bovine

## Version 0.4.0

- Changed signatures of `BovineClient` and `BovineActor` to take keyword arguments
- Document internals of `bovine.crypto`
- Add `bovine.parse`
- `BovineClient.proxy_element` renamed to just `proxy`
- `activity_factory` now has a method to create `Undo` activities
- `activity_factory` now sets `to` to the actor of a follow request for `accept`, `reject`
- Make dev, test, doc dependencies optional
- Add `bovine.crypto.build_validate_http_signature_raw`

## Version 0.3.1

- BovineClient.inbox / outbox are no longer coroutines
- BovineActor improved getting of resources
- Environment flag `BUTCHER_ALLOW_HTTP` that enables usage of http for webfinger lookup in BovineClient creation

## Version 0.3.0

- Force "items" to a `@container` of type `@set` in the `about:bovine` context
- Repair to CollectionHelper. Add collection_helper to BovineClient.

## Version 0.2.6

- Signature of `webfinger_response_json` changed (__breaking__)
- Improve addressing of object and activities. Add `as_followers` method.
- ServerSentEvent.id is now a str (was int)
- Improved CollectionHelper to be able iterate over Collection and OrderedCollection type of ActivityStreams objects.

## Version 0.2.3

- Improved REPL functionality

## Version 0.2.2

- Add command `python -mbovine.repl`.

## Version 0.2.1

- Repair jsonld request resolver

## Version 0.2.0

- Support [fep-4adb](https://codeberg.org/fediverse/fep/src/branch/main/feps/fep-4adb.md)
- Add jsonld functionality

## Version 0.1.4

- Bugfix: ObjectFactor.actor_for_mention didn't proxy the requested actor_id.

## Version 0.1.3

- Tutorial on hashtag announce bot
- Implement fep-612d
- Make `validate_moo_auth_signature` also return the domain
- Document how to get the activity id from location header after send_to_outbox

## Version 0.1.2

- Add reject to activity_factory
- Add url property to Actor
- Add python -m bovine.msg and python -m bovine.ed25519_key features

## Version 0.1.1

- Improved tutorial

## Version 0.1.0

- 2023-04-13 Added bovine.crypto module with all crypto routines, previously in bovine. Added documentation, added test cases for http signatures
- 2023-04-11 Added attachment, width, height to Object
- 2023-04-10 Activities and Objects should no longer contain empty to, cc properties
- 2023-04-09 Include sphinx.ext.viewcode in documentation

## Version 0.0.13

- 2023-04-08: Add ability to create Mention based on actor uri
- 2023-04-08: Add documentation for bovine.activitystreams.utils
- 2023-04-02: EventSource no longer returns ServerSentEvent with empty data
