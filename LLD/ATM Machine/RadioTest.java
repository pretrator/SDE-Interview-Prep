interface State {
    void play(Radio r);
    void pause(Radio r);
    void stop(Radio r);
}

class PlayingState implements State {
    @Override
    public void play(Radio r) {
        System.out.println("PLAYING -> PLAYING = Radio is already playing...");
    }

    @Override
    public void pause(Radio r) {
        System.out.println("PLAYING -> PAUSED = Radio Paused");
        r.setState(new PausedState());
    }

    @Override
    public void stop(Radio r) {
        System.out.println("PLAYING -> STOPPED = Radio Stopped");
        r.setState(new StoppedState());
    }  
}

class PausedState implements State {
    @Override
    public void play(Radio r) {
        System.out.println("PAUSED -> PLAYING = Radio is Playing");
        r.setState(new PlayingState());
    }

    @Override
    public void pause(Radio r) {
        System.out.println("PAUSED -> PAUSED = Already paused");
    }

    @Override
    public void stop(Radio r) {
        System.out.println("PAUSED -> STOPPED = Radio is Stopped");
        r.setState(new StoppedState());
    }  
}

class StoppedState implements State {
    @Override
    public void play(Radio r) {
        System.out.println("STOPPED -> PLAYING = Radio is Playing");
        r.setState(new PlayingState());
    }

    @Override
    public void pause(Radio r) {
        System.out.println("STOPPED -> PAUSED = Radio can't be paused while it is already stopped");
    }

    @Override
    public void stop(Radio r) {
        System.out.println("STOPPED -> STOPPED = Radio is already Stopped");
    }  
}

class Radio {
    State radioState;

    Radio() {
        this.radioState = new StoppedState();
    }

    public void setState(State s) {
        this.radioState = s;
    }

    public void play() {
        this.radioState.play(this);
    }

    public void pause() {
        this.radioState.pause(this);
    }
    
    public void stop() {
        this.radioState.stop(this);
    }
}

public class RadioTest {
    public static void main(String[] args) {
        Radio radio = new Radio();
        radio.play();
        radio.play();
        radio.pause();
        radio.stop();
        radio.pause();
    }    
}
