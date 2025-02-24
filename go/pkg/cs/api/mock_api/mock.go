// Code generated by MockGen. DO NOT EDIT.
// Source: github.com/scionproto/scion/go/pkg/cs/api (interfaces: BeaconStore,Healther)

// Package mock_api is a generated GoMock package.
package mock_api

import (
	context "context"
	reflect "reflect"

	gomock "github.com/golang/mock/gomock"
	api "github.com/scionproto/scion/go/pkg/cs/api"
	beacon "github.com/scionproto/scion/go/pkg/storage/beacon"
)

// MockBeaconStore is a mock of BeaconStore interface.
type MockBeaconStore struct {
	ctrl     *gomock.Controller
	recorder *MockBeaconStoreMockRecorder
}

// MockBeaconStoreMockRecorder is the mock recorder for MockBeaconStore.
type MockBeaconStoreMockRecorder struct {
	mock *MockBeaconStore
}

// NewMockBeaconStore creates a new mock instance.
func NewMockBeaconStore(ctrl *gomock.Controller) *MockBeaconStore {
	mock := &MockBeaconStore{ctrl: ctrl}
	mock.recorder = &MockBeaconStoreMockRecorder{mock}
	return mock
}

// EXPECT returns an object that allows the caller to indicate expected use.
func (m *MockBeaconStore) EXPECT() *MockBeaconStoreMockRecorder {
	return m.recorder
}

// GetBeacons mocks base method.
func (m *MockBeaconStore) GetBeacons(arg0 context.Context, arg1 *beacon.QueryParams) ([]beacon.Beacon, error) {
	m.ctrl.T.Helper()
	ret := m.ctrl.Call(m, "GetBeacons", arg0, arg1)
	ret0, _ := ret[0].([]beacon.Beacon)
	ret1, _ := ret[1].(error)
	return ret0, ret1
}

// GetBeacons indicates an expected call of GetBeacons.
func (mr *MockBeaconStoreMockRecorder) GetBeacons(arg0, arg1 interface{}) *gomock.Call {
	mr.mock.ctrl.T.Helper()
	return mr.mock.ctrl.RecordCallWithMethodType(mr.mock, "GetBeacons", reflect.TypeOf((*MockBeaconStore)(nil).GetBeacons), arg0, arg1)
}

// MockHealther is a mock of Healther interface.
type MockHealther struct {
	ctrl     *gomock.Controller
	recorder *MockHealtherMockRecorder
}

// MockHealtherMockRecorder is the mock recorder for MockHealther.
type MockHealtherMockRecorder struct {
	mock *MockHealther
}

// NewMockHealther creates a new mock instance.
func NewMockHealther(ctrl *gomock.Controller) *MockHealther {
	mock := &MockHealther{ctrl: ctrl}
	mock.recorder = &MockHealtherMockRecorder{mock}
	return mock
}

// EXPECT returns an object that allows the caller to indicate expected use.
func (m *MockHealther) EXPECT() *MockHealtherMockRecorder {
	return m.recorder
}

// GetSignerHealth mocks base method.
func (m *MockHealther) GetSignerHealth(arg0 context.Context) api.SignerHealthData {
	m.ctrl.T.Helper()
	ret := m.ctrl.Call(m, "GetSignerHealth", arg0)
	ret0, _ := ret[0].(api.SignerHealthData)
	return ret0
}

// GetSignerHealth indicates an expected call of GetSignerHealth.
func (mr *MockHealtherMockRecorder) GetSignerHealth(arg0 interface{}) *gomock.Call {
	mr.mock.ctrl.T.Helper()
	return mr.mock.ctrl.RecordCallWithMethodType(mr.mock, "GetSignerHealth", reflect.TypeOf((*MockHealther)(nil).GetSignerHealth), arg0)
}

// GetTRCHealth mocks base method.
func (m *MockHealther) GetTRCHealth(arg0 context.Context) api.TRCHealthData {
	m.ctrl.T.Helper()
	ret := m.ctrl.Call(m, "GetTRCHealth", arg0)
	ret0, _ := ret[0].(api.TRCHealthData)
	return ret0
}

// GetTRCHealth indicates an expected call of GetTRCHealth.
func (mr *MockHealtherMockRecorder) GetTRCHealth(arg0 interface{}) *gomock.Call {
	mr.mock.ctrl.T.Helper()
	return mr.mock.ctrl.RecordCallWithMethodType(mr.mock, "GetTRCHealth", reflect.TypeOf((*MockHealther)(nil).GetTRCHealth), arg0)
}
