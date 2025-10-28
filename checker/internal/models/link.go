package models

type Link struct {
	Link    string `json:"link"`
	Status  bool   `json:"status"`
	Checked bool   `json:"-"`
}

type RabbitLinks struct {
	UserId int64  `json:"user_id"`
	ChatId int64  `json:"chat_id"`
	Links  []Link `json:"links"`
}
