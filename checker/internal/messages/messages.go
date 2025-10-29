package messages

type Messenger interface {
	ReadMessages()
	ServiceMessages()
	SendMessages()

	GracefulStop()
}
