package workerPool

import (
	"context"
	"sync"

	"github.com/IvanDrf/checker/internal/models"
)

type CheckLinkFunc func(context.Context, string) bool

const maxGoroutines = 75

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

func worker(ctx context.Context, link string, out chan models.Link, checkLink CheckLinkFunc) {
	select {
	case <-ctx.Done():
		return

	default:
		out <- models.Link{
			Link:    link,
			Status:  checkLink(ctx, link),
			Checked: true,
		}
	}

}
