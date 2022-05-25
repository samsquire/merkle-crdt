# merkle-crdt
Merkle clock crdt implementation in python

# how it works

Each MerkleClock stores keyvalues or a primitive python type.

Each MerkleClock has a CID which is a hash of its children. From the hash you can retrieve all the children from the database.

I implement a total ordering over MerkleClocks by a last write wins by providing a real wall clock timestamp. If there was skew and events were concurrent, this would cause the wrong merge. Ideally this circumstance should be rare as you are relying on the hashing properties of the CRDT to merge cleanly as new CRDTs are based on the precursors or causes of that CRDT.

Each MerkleClock has inside it events that occurred before itself.
