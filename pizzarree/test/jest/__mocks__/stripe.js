import {jest} from "@jest/globals";

const  mockedStripe = jest.requireActual('@stripe/stripe-js');
let loadTestStripe = jest.spyOn(mockedStripe, 'loadStripe')
const stripeElement = {
      mount:(x)=> jest.fn(() => Promise.resolve({x})),
      unmount: jest.fn(() => Promise.resolve()),
      destroy: jest.fn(() => Promise.resolve()),
      on: jest.fn(() => Promise.resolve()),
      update: jest.fn(() => Promise.resolve()),
      off: jest.fn(() => Promise.resolve()),
      once: jest.fn(() => Promise.resolve()),
      create:(x)=>jest.fn(() => Promise.resolve(x)),
      submit:jest.fn(() => Promise.resolve()),
      show:jest.fn(() => Promise.resolve()),
      hide:jest.fn(() => Promise.resolve()),
      emit:jest.fn(() => Promise.resolve()),
      getValue:jest.fn((x) => Promise.resolve(x)),
      addEventListener:jest.fn((x) => Promise.resolve(x)),
      _registerWrapper: ()=>jest.fn(() => Promise.resolve()),
  }

const stripeMock =  Promise.resolve(loadTestStripe.mockResolvedValue({
    ...mockedStripe,
    __esModule: true,
    _api_key: 'pk_test_RUZqAN8CkTK39VGr7FuIxPWE',
    createPaymentMethod: jest.fn(() => Promise.resolve()),
    elements: () => {
      const elements = {};
      return {
        default: jest.fn(() => Promise.resolve()),
        create: jest.fn((type) => {
          elements[type] = {
              ...stripeElement
            }
          return elements[type];
        }),
        getElement: jest.fn((type) => {
          return elements[type] || null;
        }),

      }
    },
   _registerWrapper: jest.fn(() => Promise.resolve()),

  }));
  // global.window.Stripe = jest.fn(() => Promise.resolve(stripeMock));
  global.window.Stripe = stripeMock
export default stripeMock;
