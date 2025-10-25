package checker

import (
	"context"
	"sync"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

const testingTime = 10 * time.Second

func TestValidLinks(t *testing.T) {
	t.Parallel()

	validLinks := []string{
		"google.com",
		"https://ya.ru",
		"vk.com",
		"https://github.com",
	}

	ctx, cancel := context.WithTimeout(context.Background(), testingTime)
	defer cancel()

	testChecker(t, ctx, validLinks, true)
}

func TestInvalidLinks(t *testing.T) {
	t.Parallel()

	invalidLinks := []string{
		"1",
		"http://bad2.link",
		"https://httpbin.org/status/404",
		"https://httpbin.org/status/500",
	}

	ctx, cancel := context.WithTimeout(context.Background(), testingTime)
	defer cancel()

	testChecker(t, ctx, invalidLinks, false)
}

func testChecker(t *testing.T, ctx context.Context, links []string, expected bool) {
	checker := NewLinkChecker()

	wg := new(sync.WaitGroup)

	wg.Add(len(links))
	for _, link := range links {
		go func() {
			defer wg.Done()
			assert.Equal(t, expected, checker.CheckLink(ctx, link))
		}()
	}

	wg.Wait()
}
