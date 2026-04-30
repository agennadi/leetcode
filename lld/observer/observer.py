"""
Simple Observer Pattern Example

Subject (Observable): The object being observed
Observer: Objects that get notified when Subject changes
"""

from abc import ABC, abstractmethod


class Observer(ABC):
    """Observer interface"""
    @abstractmethod
    def update(self, message):
        pass


class Subject:
    """Subject (Observable) - notifies observers when state changes"""

    def __init__(self):
        self._observers = []
        self._state = None

    def attach(self, observer):
        """Add an observer"""
        self._observers.append(observer)

    def detach(self, observer):
        """Remove an observer"""
        self._observers.remove(observer)

    def notify(self, message):
        """Notify all observers"""
        for observer in self._observers:
            observer.update(message)

    def set_state(self, new_state):
        """Change state and notify observers"""
        self._state = new_state
        self.notify(f"State changed to: {new_state}")


# Concrete Observers
class EmailObserver(Observer):
    def update(self, message):
        print(f"[Email] {message}")


class SMSObserver(Observer):
    def update(self, message):
        print(f"[SMS] {message}")


# Example usage
if __name__ == "__main__":
    # Create subject
    news_agency = Subject()

    # Create observers
    email_user = EmailObserver()
    sms_user = SMSObserver()

    # Attach observers
    news_agency.attach(email_user)
    news_agency.attach(sms_user)

    # Change state - all observers get notified
    news_agency.set_state("Breaking: Python 4.0 released!")
    # Output:
    # [Email] State changed to: Breaking: Python 4.0 released!
    # [SMS] State changed to: Breaking: Python 4.0 released!

    # Detach one observer
    news_agency.detach(email_user)

    # Change state again - only remaining observer gets notified
    news_agency.set_state("Update: It was a joke!")
    # Output:
    # [SMS] State changed to: Update: It was a joke!
