# Project Notes

- Use the strategy pattern for printing out csv's based on wire mode. This will allow me to
get rid of the Cable and Wire objects, instead opting for a single Connection object.

- Consider (in the future) making the Connection object a dataclass

- Conversion plan to MVC Pattern
  - Separate the tkinter window from the main controller
  - ConnectionApp should be left with only business logic
  - ConnectionApp will now be the Controller
