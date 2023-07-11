# Project Notes

- I'm using the Factory pattern to establish a wiremanager vs a cablemanager. This isn't scalable?
- On the other hand, I still want to be able to write separate csv export functions for each. I shouldn't 
touch this code until I'm sure.

- Use the strategy pattern for printing out csv's based on wire mode. This will allow me to
get rid of the Cable and Wire objects, instead opting for a single Connection object.

- Consider (in the future) making the Connection object a dataclass