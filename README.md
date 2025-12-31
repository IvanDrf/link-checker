# Golang Link-Checker

## App

### Architecture
<details> <summary>Microservice Architecture</summary>
  <img width="800" height="500" alt="architecture" src="https://github.com/user-attachments/assets/89bff5ff-c095-49f9-b79b-b1efc389a401" />
</details>

<details> <summary>Architecture</summary>
  <br>A Clean, Onion architecture was used for each of the services.</br>
  <br></br>
  <img width="400" height="400" alt="architecture" src="https://github.com/user-attachments/assets/2241f031-ee50-4e28-ad1e-1c297831ac61" />
</details>

### Description

The application is a collection of microservices: [auth](https://github.com/IvanDrf/link-checker/tree/main/auth), [checker](https://github.com/IvanDrf/link-checker/tree/main/checker);  [http api-gateway](https://github.com/IvanDrf/link-checker/tree/main/api), [Telegram Bot](https://t.me/links_checker_chks_bot). App allows you to register by email, confirm it and check an array of links with up to 100 links in one request, or you can use [Telegram Bot](https://t.me/links_checker_chks_bot), and the checking speed is very high, because the **worker pool** pattern is used to check links.
``` go
func WorkerPool(ctx context.Context, in chan string, out chan models.Link, workers int, checkLink CheckLinkFunc) {
	wg := new(sync.WaitGroup)

	workers = min(workers, maxGoroutines)

	wg.Add(workers)
	for range workers {
		go func() {
			defer wg.Done()
			for {
				select {
				case <-ctx.Done():
					return
				default:
					link, ok := <-in
					if !ok {
						return
					}

					worker(ctx, link, out, checkLink)
				}
			}
		}()
	}

	go func() {
		wg.Wait()
		close(out)
	}()
}

```

## Documentation
The main documentation is located in the [docs/](https://github.com/IvanDrf/link-checker/tree/main/docs) directory in english and russian.

All example config files are in dirs - 'config'

## API-gateway
Documentation - [docs](https://github.com/IvanDrf/link-checker/tree/main/docs)

API routes
```go
package server

func (s *Server) RegisterRoutes() {
	s.mux.HandleFunc("POST /api/register", s.api.Register)
	s.mux.HandleFunc("/api/verify/", s.api.VerifyEmail)
	s.mux.HandleFunc("POST /api/login", s.api.Login)
	s.mux.HandleFunc("POST /api/refresh", s.api.RefreshTokens)

	s.mux.HandleFunc("POST /api/check", s.middle.AuthMiddleware(s.api.CheckLinks))
}
```

## AUTH
Proto file - [auth.proto](https://github.com/IvanDrf/link-checker/blob/main/protos/auth.proto)

## CHECKER
Proto file - [checker.proto](https://github.com/IvanDrf/link-checker/blob/main/protos/checker.proto)

## Contributing
Pull requests are welcome, but can only be merged if the code conforms to [PEP 8](https://peps.python.org/pep-0008/) for Python and [Google style guide](https://github.com/google/styleguide/tree/gh-pages/go) for GO.

