package workerPool

import (
	"checker/checker/internal/models"
	"context"
	"runtime"
	"sync"
)

var maxGoroutines = 2 * runtime.GOMAXPROCS(0)

func WorkerPool(ctx context.Context, in chan string, out chan models.Url, checkUrl func(context.Context, string) bool) {
	wg := new(sync.WaitGroup)

	for range maxGoroutines {
		for url := range in {
			wg.Add(1)
			go func() {
				defer wg.Done()
				worker(ctx, url, out, checkUrl)
			}()
		}
	}

	go func() {
		wg.Wait()
		close(out)
	}()
}

func worker(ctx context.Context, url string, out chan models.Url, checkUrl func(context.Context, string) bool) {
	select {
	case <-ctx.Done():
		return

	default:
		out <- models.Url{
			Url:    url,
			Status: checkUrl(ctx, url),
		}
	}

}
