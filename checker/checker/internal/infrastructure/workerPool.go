package workerPool

import (
	"checker/checker/internal/models"
	"context"
	"sync"
)

const maxGoroutines = 50

func WorkerPool(ctx context.Context, in chan string, out chan models.Link, checkLink func(context.Context, string) bool) {
	wg := new(sync.WaitGroup)

	wg.Add(maxGoroutines)
	for range maxGoroutines {
		go func() {
			defer wg.Done()

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

		}()
	}

	go func() {
		wg.Wait()
		close(out)
	}()
}

func worker(ctx context.Context, link string, out chan models.Link, checkLink func(context.Context, string) bool) {
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
