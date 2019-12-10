package main

type kvs struct {
	dict map[string]string
}

// create new key value store
func newKvs() *kvs {
	k := new(kvs)
	k.dict = make(map[string]string)
	return k
}

func (k *kvs) get(key string) string {
	return k.dict[key]
}

func (k *kvs) put(key, value string) {
	k.dict[key] = value
}

func (k *kvs) isKeyExist(key string) bool {
	_, isKeyExist := k.dict[key]
	return isKeyExist
}

func (k *kvs) deleteKey(key string) {
	delete(k.dict, key)
}

func (k *kvs) isKeyValid(key string) bool {
	length := len(key)
	if length < 1 || length > 200 {
		return false
	}
	return true
}
