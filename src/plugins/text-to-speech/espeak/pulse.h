#ifndef __SRS_ESPEAK_PULSE_H__
#define __SRS_ESPEAK_PULSE_H__

#include <stdint.h>
#include <murphy/common/macros.h>
#include <pulse/pulseaudio.h>

#include "srs/daemon/voice.h"

MRP_CDECL_BEGIN

/*
 * PA stream events
 */

typedef enum {
    PULSE_STREAM_NONE      = SRS_VOICE_EVENT_STARTED - 1,
    PULSE_STREAM_STARTED   = SRS_VOICE_EVENT_STARTED,
    PULSE_STREAM_PROGRESS  = SRS_VOICE_EVENT_PROGRESS,
    PULSE_STREAM_COMPLETED = SRS_VOICE_EVENT_COMPLETED,
    PULSE_STREAM_TIMEOUT   = SRS_VOICE_EVENT_TIMEOUT,
    PULSE_STREAM_ABORTED   = SRS_VOICE_EVENT_ABORTED,
    PULSE_STREAM_CORKED,
    PULSE_STREAM_UNCORKED,
} pulse_stream_event_type_t;

#define PULSE_MASK_NONE      SRS_VOICE_MASK_NONE
#define PULSE_MASK_STARTED   SRS_VOICE_MASK_STARTED
#define PULSE_MASK_PROGRESS  SRS_VOICE_MASK_PROGRESS
#define PULSE_MASK_COMPLETED SRS_VOICE_MASK_COMPLETED
#define PULSE_MASK_ABORTED   SRS_VOICE_MASK_ABORTED
#define PULSE_MASK_CORKED    (1 << PULSE_STREAM_CORKED)
#define PULSE_MASK_UNCORKED  (1 << PULSE_STREAM_UNCORKED)
#define PULSE_MASK_ONESHOT   (~(PULSE_MASK_PROGRESS))
#define PULSE_MASK_ALL       (PULSE_MASK_STARTED | PULSE_MASK_PROGRESS | \
                              PULSE_MASK_COMPLETED | PULSE_MASK_ABORTED)

typedef struct pulse_s pulse_t;

typedef srs_voice_event_t pulse_stream_event_t;

typedef void (*pulse_stream_cb_t)(pulse_t *p, pulse_stream_event_t *event,
                                  void *user_data);

/** Set up the PulseAudio interface. */
pulse_t *pulse_setup(pa_mainloop_api *pa, const char *name);

/** Clean up the audio interface. */
void pulse_cleanup(pulse_t *p);

/** Render an stream (a buffer of audio samples). */
uint32_t pulse_play_stream(pulse_t *p, void *sample_buf, int sample_rate,
                           int nchannel, uint32_t nsample, char **tags,
                           int event_mask, pulse_stream_cb_t cb,
                           void *user_data);

/** Stop an ongoing stream. */
int pulse_stop_stream(pulse_t *p, uint32_t id, int drain, int notify);

MRP_CDECL_END

#endif /* __SRS_ESPEAK_PULSE_H__ */
