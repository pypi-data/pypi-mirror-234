use traiter::numbers::Parity;

pub(super) type Event = usize;

pub(super) fn is_event_left(event: Event) -> bool {
    event.is_even()
}

pub(super) fn segment_id_to_left_event(segment_id: usize) -> Event {
    segment_id * 2
}

pub(super) fn segment_id_to_right_event(segment_id: usize) -> Event {
    segment_id * 2 + 1
}
