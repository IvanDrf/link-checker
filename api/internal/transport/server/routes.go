package server

func (s *Server) RegisterRoutes() {
	s.mux.HandleFunc("POST /api/register", s.api.Register)
	s.mux.HandleFunc("/api/verify/", s.api.VerifyEmail)
	s.mux.HandleFunc("POST /api/login", s.api.Login)
	s.mux.HandleFunc("POST /api/refresh", s.api.RefreshTokens)

	s.mux.HandleFunc("POST /api/check", s.middle.AuthMiddleware(s.api.CheckLinks))
}
