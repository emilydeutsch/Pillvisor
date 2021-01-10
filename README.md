# Pillvisor

## External Links

Devpost submission can be found [here](https://devpost.com/software/pillvisor)

The machine learning model file is too large to go on github so it can be downloaded [here](https://drive.google.com/file/d/1qQHHHWDjcuoMhbA4IO3vB0hAMtF27dce/view?usp=sharing)

## Inspiration

Adults over the age of 50 take an average of 15 prescription medications annually. Keeping track of this is very challenging. 
Pillvisor is a smart pillbox that solves the issue of medication error by verifying the pills are taken correctly in order to keep your loved ones safe. Unlike other products on the market, pillvisor integrates with a real pillbox and is designed with senior users in mind. 

 As we can imagine, keeping track of the pill schedule is challenging and taking incorrect medications can lead to serious avoidable complications. The most common drugs taken at home that have serious complications from medication errors are cardiovascular drugs and painkillers. 

One study found that almost a third of a million Americans contact poison control annually due to medication errors taken at home. One third of the errors result in hospital admissions whose admittance in on a steady rise. This only includes at home errors while medication errors can also occur in health care facilities. 

## What it does

Pillvisor is an automated pill box supervisor designed to help people who take many medications on the daily to ensure they actually take the correct pills at the correct time. Unlike many reminder and alarm apps that are wildly available on the app store, our custom pillbox product actually checks that pills are taken so the alarm isn't just turned off and ignored.  

## How we built it

Our blacked out pillbox uses photo-resistors to detect which day is open and this verifies the pill is removed from the correct day and it does not stop the alarm if an incorrect day is opened. Once the medication is removed a photo of the medication is taken to check that it is indeed the correct medication, otherwise the user will be reminded to try to scan another pill.  

We have green LEDs to indicate the correct day of the week. If the user opens an incorrect day or scans the wrong pill a red LED will flash to alert the user. An LCD display to show the medication name and instructions for using the system. 

We used tensorflow to develop a machine learning convolutional neural network for image recognition to distinguish the different pills from one another. Our Raspberry PI takes a photo, runs the neural network on it and checks to see if the correct pill has been photographed.
For our user interface, We developed an isolated Flask application which is connected to our firebase database and allows alarms to be set, deleted and edited  easily and quickly(for example changing the time or day of a certain alarm). A sync button on the raspberry pi allows it to be constantly up to date with the backend database after changes are made on the cloud.


## Challenges we ran into
Due to the complexity of the project, we ran into many issues with both software and hardware. Our biggest challenge for the project was getting the image recognition to work, and produce accurate results due to noise coming from the hand holding the pill. Additionally, getting all the packages and dependencies such as tensorflow and opencv installed onto the system our posed to be a huge challenge

On the hardware side, we ran into issues detecting if the pillbox is opened or closed based on the imperfection in ‘blacking out’ the pillbox. Due to constraints we didn’t have an opaque box.

## Accomplishments that we’re proud of

We did this hackathon to challenge ourselves to use and apply our skills to new technologies that we were unfamiliar with or relatively new with such as databases, flask, machine learning, and hardware. Additionally, this was the first hackathon for 2 of our team members and we are very proud of what we achieved and what we have learned in such a short period of time. We were happy that we were able to integrate hardware and software together for this project and apply our skills from our varying engineering backgrounds.

## What I learned

- How to setup a database
- Machine learning, tensorflow, convolutional neural networks
- Using Flask

## What's next for Pillviser

Due to time constraints, we were unable to implement all the features we wanted.
One feature we still need to add is a snooze feature to allow a delay of the alarm by a set amount of time which is useful especially if the medication has eating constraints with it. 

Additionally, we want to improve the image recognition on the pills which we believe can be made into a seperate program would be highly valuable in healthcare facilities as a last line of defence as pills are normally handled using patient charts and delivered through a chain of people so it can be an extra line of defence. 
