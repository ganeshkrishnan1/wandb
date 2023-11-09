// Code generated by mockery v2.36.1. DO NOT EDIT.

package server

import (
	mock "github.com/stretchr/testify/mock"

	service "github.com/wandb/wandb/nexus/pkg/service"
)

// MockHandlerInterface is an autogenerated mock type for the HandlerInterface type
type MockHandlerInterface struct {
	mock.Mock
}

type MockHandlerInterface_Expecter struct {
	mock *mock.Mock
}

func (_m *MockHandlerInterface) EXPECT() *MockHandlerInterface_Expecter {
	return &MockHandlerInterface_Expecter{mock: &_m.Mock}
}

// Close provides a mock function with given fields:
func (_m *MockHandlerInterface) Close() {
	_m.Called()
}

// MockHandlerInterface_Close_Call is a *mock.Call that shadows Run/Return methods with type explicit version for method 'Close'
type MockHandlerInterface_Close_Call struct {
	*mock.Call
}

// Close is a helper method to define mock.On call
func (_e *MockHandlerInterface_Expecter) Close() *MockHandlerInterface_Close_Call {
	return &MockHandlerInterface_Close_Call{Call: _e.mock.On("Close")}
}

func (_c *MockHandlerInterface_Close_Call) Run(run func()) *MockHandlerInterface_Close_Call {
	_c.Call.Run(func(args mock.Arguments) {
		run()
	})
	return _c
}

func (_c *MockHandlerInterface_Close_Call) Return() *MockHandlerInterface_Close_Call {
	_c.Call.Return()
	return _c
}

func (_c *MockHandlerInterface_Close_Call) RunAndReturn(run func()) *MockHandlerInterface_Close_Call {
	_c.Call.Return(run)
	return _c
}

// GetRun provides a mock function with given fields:
func (_m *MockHandlerInterface) GetRun() *service.RunRecord {
	ret := _m.Called()

	var r0 *service.RunRecord
	if rf, ok := ret.Get(0).(func() *service.RunRecord); ok {
		r0 = rf()
	} else {
		if ret.Get(0) != nil {
			r0 = ret.Get(0).(*service.RunRecord)
		}
	}

	return r0
}

// MockHandlerInterface_GetRun_Call is a *mock.Call that shadows Run/Return methods with type explicit version for method 'GetRun'
type MockHandlerInterface_GetRun_Call struct {
	*mock.Call
}

// GetRun is a helper method to define mock.On call
func (_e *MockHandlerInterface_Expecter) GetRun() *MockHandlerInterface_GetRun_Call {
	return &MockHandlerInterface_GetRun_Call{Call: _e.mock.On("GetRun")}
}

func (_c *MockHandlerInterface_GetRun_Call) Run(run func()) *MockHandlerInterface_GetRun_Call {
	_c.Call.Run(func(args mock.Arguments) {
		run()
	})
	return _c
}

func (_c *MockHandlerInterface_GetRun_Call) Return(_a0 *service.RunRecord) *MockHandlerInterface_GetRun_Call {
	_c.Call.Return(_a0)
	return _c
}

func (_c *MockHandlerInterface_GetRun_Call) RunAndReturn(run func() *service.RunRecord) *MockHandlerInterface_GetRun_Call {
	_c.Call.Return(run)
	return _c
}

// Handle provides a mock function with given fields:
func (_m *MockHandlerInterface) Handle() {
	_m.Called()
}

// MockHandlerInterface_Handle_Call is a *mock.Call that shadows Run/Return methods with type explicit version for method 'Handle'
type MockHandlerInterface_Handle_Call struct {
	*mock.Call
}

// Handle is a helper method to define mock.On call
func (_e *MockHandlerInterface_Expecter) Handle() *MockHandlerInterface_Handle_Call {
	return &MockHandlerInterface_Handle_Call{Call: _e.mock.On("Handle")}
}

func (_c *MockHandlerInterface_Handle_Call) Run(run func()) *MockHandlerInterface_Handle_Call {
	_c.Call.Run(func(args mock.Arguments) {
		run()
	})
	return _c
}

func (_c *MockHandlerInterface_Handle_Call) Return() *MockHandlerInterface_Handle_Call {
	_c.Call.Return()
	return _c
}

func (_c *MockHandlerInterface_Handle_Call) RunAndReturn(run func()) *MockHandlerInterface_Handle_Call {
	_c.Call.Return(run)
	return _c
}

// SetInboundChannels provides a mock function with given fields: in, lb, slb
func (_m *MockHandlerInterface) SetInboundChannels(in <-chan *service.Record, lb <-chan *service.Record, slb chan *service.Record) {
	_m.Called(in, lb, slb)
}

// MockHandlerInterface_SetInboundChannels_Call is a *mock.Call that shadows Run/Return methods with type explicit version for method 'SetInboundChannels'
type MockHandlerInterface_SetInboundChannels_Call struct {
	*mock.Call
}

// SetInboundChannels is a helper method to define mock.On call
//   - in <-chan *service.Record
//   - lb <-chan *service.Record
//   - slb chan *service.Record
func (_e *MockHandlerInterface_Expecter) SetInboundChannels(in interface{}, lb interface{}, slb interface{}) *MockHandlerInterface_SetInboundChannels_Call {
	return &MockHandlerInterface_SetInboundChannels_Call{Call: _e.mock.On("SetInboundChannels", in, lb, slb)}
}

func (_c *MockHandlerInterface_SetInboundChannels_Call) Run(run func(in <-chan *service.Record, lb <-chan *service.Record, slb chan *service.Record)) *MockHandlerInterface_SetInboundChannels_Call {
	_c.Call.Run(func(args mock.Arguments) {
		run(args[0].(<-chan *service.Record), args[1].(<-chan *service.Record), args[2].(chan *service.Record))
	})
	return _c
}

func (_c *MockHandlerInterface_SetInboundChannels_Call) Return() *MockHandlerInterface_SetInboundChannels_Call {
	_c.Call.Return()
	return _c
}

func (_c *MockHandlerInterface_SetInboundChannels_Call) RunAndReturn(run func(<-chan *service.Record, <-chan *service.Record, chan *service.Record)) *MockHandlerInterface_SetInboundChannels_Call {
	_c.Call.Return(run)
	return _c
}

// SetOutboundChannels provides a mock function with given fields: fwd, out
func (_m *MockHandlerInterface) SetOutboundChannels(fwd chan *service.Record, out chan *service.Result) {
	_m.Called(fwd, out)
}

// MockHandlerInterface_SetOutboundChannels_Call is a *mock.Call that shadows Run/Return methods with type explicit version for method 'SetOutboundChannels'
type MockHandlerInterface_SetOutboundChannels_Call struct {
	*mock.Call
}

// SetOutboundChannels is a helper method to define mock.On call
//   - fwd chan *service.Record
//   - out chan *service.Result
func (_e *MockHandlerInterface_Expecter) SetOutboundChannels(fwd interface{}, out interface{}) *MockHandlerInterface_SetOutboundChannels_Call {
	return &MockHandlerInterface_SetOutboundChannels_Call{Call: _e.mock.On("SetOutboundChannels", fwd, out)}
}

func (_c *MockHandlerInterface_SetOutboundChannels_Call) Run(run func(fwd chan *service.Record, out chan *service.Result)) *MockHandlerInterface_SetOutboundChannels_Call {
	_c.Call.Run(func(args mock.Arguments) {
		run(args[0].(chan *service.Record), args[1].(chan *service.Result))
	})
	return _c
}

func (_c *MockHandlerInterface_SetOutboundChannels_Call) Return() *MockHandlerInterface_SetOutboundChannels_Call {
	_c.Call.Return()
	return _c
}

func (_c *MockHandlerInterface_SetOutboundChannels_Call) RunAndReturn(run func(chan *service.Record, chan *service.Result)) *MockHandlerInterface_SetOutboundChannels_Call {
	_c.Call.Return(run)
	return _c
}

// NewMockHandlerInterface creates a new instance of MockHandlerInterface. It also registers a testing interface on the mock and a cleanup function to assert the mocks expectations.
// The first argument is typically a *testing.T value.
func NewMockHandlerInterface(t interface {
	mock.TestingT
	Cleanup(func())
}) *MockHandlerInterface {
	mock := &MockHandlerInterface{}
	mock.Mock.Test(t)

	t.Cleanup(func() { mock.AssertExpectations(t) })

	return mock
}
