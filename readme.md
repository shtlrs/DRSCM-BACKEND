# DRSCM

> Disclaimer: Only the backend is usable at this point.

DRSCM, or Dulmen Regulatory Services Client Manager, is a hobby application developed for a friend of mine that used to time track
and make his invoices by hand in his office on Saturdays/Sundays.

This was time consuming for him, error prone (because it took time, so focus was lost), and not so practical.

I had proposed to develop DRSCM in order to help him with that.

This used to be a Desktop app, and was the first app I had ever made.

Looking back at it, it was quite "chonky", so I decided to rewrite it as a web app, and publish it here.

The application is quite simple, it:
* Allows to add a list of `Client`s
* Assigns multiple `Project`s to a specific `Client`
* Time tracks the work being done on a `Project` via `WorkSession`s.
* Generates `Invoice`s depending on specific business rules for a `Client`.