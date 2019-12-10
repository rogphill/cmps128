package main

type successDelMsg struct {
	Msg string `json:"msg"`
}

type resultMsg struct {
	Result string `json:"result"`
	Msg    string `json:"msg"`
}

type msgExists struct {
	IsExist string `json:"isExist"`
	Msg     string `json:"msg"`
}

type resultValue struct {
	Result string `json:"result"`
	Value  string `json:"value"`
}

type replacedMsg struct {
	Replaced bool   `json:"replaced"`
	Msg      string `json:"msg"`
}

type msgValue struct {
	Msg   string `json:"msg"`
	Value string `json:"value"`
}

type msgError struct {
	Msg   string `json:"msg"`
	Error string `json:"error"`
}
