package main

import (
	"strings"
)

type set struct {
	Set map[string]int
}

func newSet(view string) *set {
	s := new(set)
	s.Set = make(map[string]int)
	if view != "" {
		views := strings.Split(view, ",")
		for _, v := range views {
			s.put(v)
		}
	}
	return s
}

func (s *set) isExist(key string) bool {
	_, isExist := s.Set[key]
	return isExist
}

func (s *set) put(key string) {
	s.Set[key] = 0
}

func (s *set) get(key string) int {
	return s.Set[key]
}

func (s *set) delete(key string) {
	delete(s.Set, key)
}
