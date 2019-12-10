package main

import (
	"encoding/json"
	"log"
	"os"
	"time"
)

type kvs struct {
	Dict map[string]valueVectorClock
}

type valueVectorClock struct {
	Value       string
	VectorClock *set
	TimeStamp   time.Time
}

// create new key Value store
func newKvs() *kvs {
	k := new(kvs)
	k.Dict = make(map[string]valueVectorClock)
	return k
}

func (k *kvs) get(key string) string {
	log.Println(k.Dict[key].Value)
	return k.Dict[key].Value
}
func (k *kvs) getVectorClock(key string) *set {
	return k.Dict[key].VectorClock
}
func (k *kvs) setVectorClock(key string, val int) {
	k.Dict[key].VectorClock.Set[iPPort] = val
}
func (k *kvs) getTimeStamp(key string) time.Time {
	return k.Dict[key].TimeStamp
}

// TODO: VC  is not updated when key replaced
func (k *kvs) put(key, value string, timeStamp time.Time) {
	if !k.isKeyExist(key) {
		k.Dict[key] = valueVectorClock{
			Value:       value,
			VectorClock: newSet(os.Getenv("VIEW")),
			TimeStamp:   timeStamp,
		}
	} else {
		k.Dict[key] = valueVectorClock{
			Value:       value,
			VectorClock: k.Dict[key].VectorClock,
			TimeStamp:   timeStamp,
		}
	}

}

func (k *kvs) isKeyExist(key string) bool {
	_, isKeyExist := k.Dict[key]
	return isKeyExist
}

func (k *kvs) deleteKey(key string) {
	delete(k.Dict, key)
}

func (k *kvs) incVectorClock(key string) {
	clock := k.getVectorClock(key).Set[iPPort]
	clock++
	k.setVectorClock(key, clock)
}

func (k *kvs) mergeVectorClock(whichKey string, v string) {
	myVectorClock := k.getVectorClock(whichKey)
	tempVectorClock := newSet("")
	json.Unmarshal([]byte(v), &tempVectorClock.Set)
	for key, clock := range tempVectorClock.Set {
		if myVectorClock.isExist(key) {
			if myVectorClock.get(key) < clock {
				myVectorClock.Set[key] = clock
			}
		}
	}
}

func (k *kvs) convertVCtoString(key string) string {
	encodeView, _ := json.Marshal(k.getVectorClock(key).Set)
	return string(encodeView)
}

func (k *kvs) convertStringtoVC(payload []byte) map[string]int {
	var vectorClock map[string]int
	json.Unmarshal(payload, &vectorClock)
	return vectorClock
}
