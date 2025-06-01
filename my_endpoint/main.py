from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from ag_ui.core import RunAgentInput, Message, EventType, RunStartedEvent, RunFinishedEvent
from ag_ui.encoder import EventEncoder

app = FastAPI(title="AG-UI Endpoint")

@app.post("/awp")
async def my_endpoint(input_data: RunAgentInput):
    async def event_generator():
        # Create an event encoder to properly format SSE events
        encoder = EventEncoder()

        # Send run started event
        yield encoder.encode(
          RunStartedEvent(
            type=EventType.RUN_STARTED,
            thread_id=input_data.thread_id,
            run_id=input_data.run_id
          )
        )

        # Send run finished event
        yield encoder.encode(
          RunFinishedEvent(
            type=EventType.RUN_FINISHED,
            thread_id=input_data.thread_id,
            run_id=input_data.run_id
          )
        )

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)