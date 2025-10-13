package linkService

import "checker/checker/internal/models"

type Linker interface {
	CheckLinks(links []string) ([]models.Link, error)
}

type linker struct {
}

func NewLinker() Linker {
	return &linker{}
}

func (l *linker) CheckLinks(links []string) ([]models.Link, error) {
	return nil, nil
}
